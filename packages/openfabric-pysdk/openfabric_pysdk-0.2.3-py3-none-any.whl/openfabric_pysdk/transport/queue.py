import uuid

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import fields

from openfabric_pysdk.engine import background
from openfabric_pysdk.loader import *
from openfabric_pysdk.context import RaySchema, State


#######################################################
#  Execution Queue Result API
#######################################################

class QueueApi_Get(MethodResource, Resource):
    __state: State = None

    # ------------------------------------------------------------------------
    def __init__(self, state: State = None):
        self.__state = state

    @doc(description="Get the response for the indicated request", tags=["Queue"])
    @use_kwargs({'qid': fields.String(required=True)}, location='query')
    @marshal_with(OutputSchema)  # marshalling
    def get(self, qid: str, *args) -> OutputClass:
        return background.read(qid, 'out', OutputSchema().load)


class QueueApi_Delete(MethodResource, Resource):
    __state: State = None

    # ------------------------------------------------------------------------
    def __init__(self, state: State = None):
        self.__state = state

    @doc(description="Remove the indicated requests and the associated results", tags=["Queue"])
    @use_kwargs({'qid': fields.String(required=True)}, location='query')
    @marshal_with(RaySchema)
    def delete(self, qid: str, *args):
        return background.delete(qid)


class QueueApi_List(MethodResource, Resource):
    __state: State = None

    # ------------------------------------------------------------------------
    def __init__(self, state: State = None):
        self.__state = state

    @doc(description="Get list of existing requests and their status", tags=["Queue"])
    @marshal_with(RaySchema(many=True))
    def get(self, *args):
        return background.rays()


class QueueApi_Post(MethodResource, Resource):
    __state: State = None

    # ------------------------------------------------------------------------
    def __init__(self, state: State = None):
        self.__state = state

    @doc(description="Queue a new request", tags=["Queue"])
    @use_kwargs(InputSchema, location='json')
    @marshal_with(RaySchema)
    def post(self, *args):
        data = InputSchema().dump(list(args) if InputSchema().many is True else args[0])
        sid = uuid.uuid4().hex
        uid = uuid.uuid4().hex
        qid = background.prepare(data, sid=sid, uid=uid, state=self.__state)
        ray = background.ray(qid)
        return ray
