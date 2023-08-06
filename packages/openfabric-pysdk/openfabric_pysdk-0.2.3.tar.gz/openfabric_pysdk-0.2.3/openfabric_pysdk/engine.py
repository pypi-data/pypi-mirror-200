import logging
import os
import threading
import traceback
import uuid
from time import sleep
from typing import Dict, Any, List

from openfabric_pysdk.benchmark import MeasureBlockTime
from openfabric_pysdk.context import RayStatus, Ray, RaySchema, State
from openfabric_pysdk.loader import InputSchema, execution_callback_function, OutputSchema
from openfabric_pysdk.store import Store
from openfabric_pysdk.task import Task


#######################################################
#  Foreground Engine
#######################################################
class ForegroundEngine:
    __store: Store = None
    __state: State = None
    __rays: Dict[str, Ray] = None

    # ------------------------------------------------------------------------
    def __init__(self):
        self.__rays = dict()
        self.__store = Store(path=f"{os.getcwd()}/datastore")

    # ------------------------------------------------------------------------
    def prepare(self, data: str, qid=None, sid=None, uid=None, state: State = None) -> str:
        if qid is None:
            qid: str = uuid.uuid4().hex
        ray = self.ray(qid)
        ray.status = RayStatus.QUEUED
        ray.sid = sid
        ray.uid = uid
        self.write(qid, 'ray', ray, RaySchema().dump)
        self.write(qid, 'in', data)
        self.__state = state
        return qid

    # ------------------------------------------------------------------------
    def ray(self, qid: str):
        if self.__rays.get(qid) is None:
            ray = Ray(qid=qid)
            self.__rays[qid] = ray
        return self.__rays[qid]

    # ------------------------------------------------------------------------
    def rays(self, criteria=None) -> List[Ray]:
        rays: List[Ray] = []
        for qid, ray in self.__rays.items():
            if criteria is None or criteria(ray):
                rays.append(ray)
        return rays

    # ------------------------------------------------------------------------
    def process(self, qid):

        with MeasureBlockTime("Engine::execution_callback_function"):

            output = None
            ray = self.ray(qid)
            try:
                data = self.read(qid, 'in', InputSchema().load)
                if data is None:
                    return None

                ray.status = RayStatus.RUNNING
                self.write(qid, 'ray', ray, RaySchema().dump)
                output = execution_callback_function(data, ray, self.__state)
                ray.status = RayStatus.COMPLETED
                ray.progress(step=100)
            except Exception as e:
                logging.error(f"Openfabric - failed executing: [{qid}]{e}")
                traceback.print_exc()
                ray.status = RayStatus.FAILED
        ray.finished = True
        self.write(qid, 'ray', ray, RaySchema().dump)
        self.write(qid, 'out', output, OutputSchema().dump)

        return output

    # ------------------------------------------------------------------------
    def read(self, qid: str, key: str, deserializer=None) -> Any:
        output = self.__store.get(qid, key)
        if output is None:
            return None
        output = deserializer(output) if deserializer is not None else output
        return output

    # ------------------------------------------------------------------------
    def write(self, qid: str, key: str, val: Any, serializer=None):
        if val is not None:
            val = serializer(val) if serializer is not None else val
        self.__store.set(qid, key, val)

    # ------------------------------------------------------------------------
    def delete(self, qid: str) -> Ray:
        ray = self.ray(qid)
        self.__store.drop(qid)
        ray.status = RayStatus.REMOVED
        return ray


#######################################################
#  Background Engine
#######################################################
class BackgroundEngine:
    __task: Task = None
    __instances: int = 0
    __running: bool = False
    __current_qid: str = None
    __worker: threading.Thread = None
    __lock: threading.Condition = threading.Condition()

    # ------------------------------------------------------------------------
    def __init__(self):
        self.__lock.acquire()
        if self.__instances == 0:
            self.__task = Task()
            self.__worker = threading.Thread(target=self.__process, args=())
            self.__worker.start()

        self.__instances = self.__instances + 1
        self.__lock.release()

        # Wait for processing thread to start
        while not self.__running:
            sleep(0.1)

    # ------------------------------------------------------------------------
    def __del__(self):
        self.__lock.acquire()
        if self.__instances > 0:
            self.__lock.release()
            return

        self.__running = False

        self.__lock.notify_all()
        self.__lock.release()

    # ------------------------------------------------------------------------
    def __process(self):
        self.__running = True
        while self.__running:
            self.__lock.acquire()
            self.__current_qid = None
            while self.__running and self.__task.empty():
                self.__lock.wait()
            try:
                self.__current_qid = self.__task.next()
            except:
                logging.warning("Openfabric - queue empty!")
                traceback.print_exc()
            finally:
                self.__lock.release()

            if self.__running and self.__current_qid is not None:
                foreground.process(self.__current_qid)

    # ------------------------------------------------------------------------
    def prepare(self, data: str, qid=None, sid=None, uid=None, state: State = None) -> str:
        self.__lock.acquire()
        qid: str = foreground.prepare(data, qid=qid, sid=sid, uid=uid, state=state)
        self.__task.add(qid)
        self.__lock.notify_all()
        self.__lock.release()
        return qid

    # ------------------------------------------------------------------------
    def ray(self, qid: str) -> Ray:
        return foreground.ray(qid)

    # ------------------------------------------------------------------------
    def rays(self, criteria=None) -> List[str]:
        rays: List[str] = []
        for qid in self.__task.all():
            ray = foreground.read(qid, 'ray', RaySchema().load)
            if criteria is None or criteria(ray):
                rays.append(ray)
        rays.sort(key=lambda r: r.created_at)
        return rays

    # ------------------------------------------------------------------------
    def delete(self, qid: str) -> Ray:
        self.__lock.acquire()
        self.__task.rem(qid)
        ray = foreground.delete(qid)
        self.__lock.notify_all()
        self.__lock.release()
        return ray

    # ------------------------------------------------------------------------
    def read(self, qid: str, key: str, deserializer=None) -> Any:
        return foreground.read(qid, key, deserializer)

    # ------------------------------------------------------------------------
    def write(self, qid: str, key: str, val: Any, serializer=None):
        return foreground.write(qid, key, val, serializer)


foreground = ForegroundEngine()
background = BackgroundEngine()
