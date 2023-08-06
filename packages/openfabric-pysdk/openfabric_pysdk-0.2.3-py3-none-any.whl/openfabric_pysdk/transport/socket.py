import json
import logging
import zlib
from hashlib import md5

from typing import Any, Set, Dict

import eventlet
from flask import Flask, request
from flask_socketio import SocketIO, Namespace, emit

from openfabric_pysdk.context import RaySchema, Ray, State, StateSchema
from openfabric_pysdk.engine import foreground, background
from openfabric_pysdk.loader import *
from openfabric_pysdk.utility import ChangeDetector


#######################################################
#  Execution Socket
#######################################################
class Socket(Namespace):
    __app = None
    __state = None
    __session = None
    __socket_io = None
    __active_sessions: Set[str] = None

    # ------------------------------------------------------------------------
    def __init__(self, socket_namespace, socket_session, app: Flask, state: State):
        super().__init__(socket_namespace)
        self.__session = socket_session
        # Set this variable to "threading", "eventlet" or "gevent" to test the
        # different async modes, or leave it set to None for the application to choose
        # the best option based on installed packages.
        async_mode = "eventlet"
        self.__socket_io = SocketIO(app, async_mode=async_mode, cors_allowed_origins='*')
        self.__socket_io.on_namespace(self)
        self.__app = app
        self.__state = state
        self.__active_sessions = set()

    # ------------------------------------------------------------------------
    def run(self, debug, host, port):
        self.__socket_io.run(self.__app, host=host, debug=debug, port=port)

    # ------------------------------------------------------------------------
    def on_execute(self, data: Any, background: bool):
        with MeasureBlockTime("Socket::execute"):
            # Uncompress data
            with MeasureBlockTime("Socket::decompress"):
                uncompressed = zlib.decompress(data)
                request_payload: str = uncompressed.decode('utf-8')
                dictionary: Dict[str, Any] = json.loads(request_payload)

            sid = request.sid
            data = dictionary.get('body', None)
            header = dictionary.get('header', dict())
            uid = header.get('uid', None)

            if background is True:
                self.__execute_background(data, sid, uid)
            else:
                self.__execute_foreground(data, sid, uid)

    def __execute_foreground(self, data: str, sid: str, uid: str):
        # Setup
        qid = foreground.prepare(data, qid=sid, sid=sid, uid=uid, state=self.__state)
        ray = foreground.ray(qid)
        # Execute in foreground
        with MeasureBlockTime("Socket::callback"):
            foreground.process(qid)
            output = foreground.read(qid, 'out')
            ray_dump = RaySchema().dump(ray)
            foreground.delete(qid)
            emit('response', dict(output=output, ray=ray_dump))

    def __execute_background(self, data: str, sid: str, uid: str):
        # Setup
        qid = background.prepare(data, sid=sid, uid=uid, state=self.__state)
        ray = background.ray(qid)
        emit('submitted', RaySchema().dump(ray))
        # Execute in background
        with MeasureBlockTime("Socket::callback"):
            while sid in self.__active_sessions:
                ray_dump = RaySchema().dump(ray)
                emit('progress', ray_dump)
                if ray.finished is True:
                    # input = background.get(qid, 'in')
                    output = background.read(qid, 'out')
                    emit('response', dict(output=output, ray=ray_dump))
                    break
                eventlet.sleep(0.1)

    # ------------------------------------------------------------------------
    def on_resume(self, uid: str):
        sid = request.sid
        with MeasureBlockTime("OpenfabricSocket::restore"):
            def criteria(_ray: Ray):
                # is deleted ?
                if _ray is None:
                    return False
                # is different user ?
                if _ray.uid != uid:
                    return False
                # is an active session available ?
                if _ray.sid in self.__active_sessions and _ray.sid != sid:
                    return False
                return True

            # Filter rays
            rays = background.rays(criteria)
            for ray in rays:
                emit('progress', RaySchema().dump(ray))

    # ------------------------------------------------------------------------
    def on_restore(self, qid: str):
        ray_dump = foreground.read(qid, 'ray')
        input_dump = foreground.read(qid, 'in')
        output_dump = foreground.read(qid, 'out')
        emit('restore', dict(input=input_dump, output=output_dump, ray=ray_dump))

    # ------------------------------------------------------------------------
    def on_state(self, uid: str):
        sid = request.sid
        with MeasureBlockTime("Socket::state"):
            while sid in self.__active_sessions:
                changed = ChangeDetector.is_changed('app::state' + sid, self.__state, StateSchema().dump)
                if changed is True:
                    emit('state', StateSchema().dump(self.__state))
                eventlet.sleep(0.1)

    # ------------------------------------------------------------------------
    def on_delete(self, qid: str):
        sid = request.sid
        with MeasureBlockTime("OpenfabricSocket::delete"):
            foreground.delete(qid)
            background.delete(qid)

    # ------------------------------------------------------------------------
    def on_connect(self):
        sid = request.sid
        logging.debug(f'Openfabric - client connected {sid} on {request.host}')
        self.__active_sessions.add(sid)

    # ------------------------------------------------------------------------
    def on_disconnect(self):
        sid = request.sid
        logging.debug(f'Openfabric - client disconnected {sid} on {request.host}')
        self.__active_sessions.remove(sid)
