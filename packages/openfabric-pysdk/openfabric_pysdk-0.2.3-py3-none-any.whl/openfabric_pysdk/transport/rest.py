import uuid

from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from flask_restful import Resource

from openfabric_pysdk.engine import foreground
from openfabric_pysdk.loader import *
from openfabric_pysdk.context import State


#######################################################
#  Execution API
#######################################################
class ExecutionRestApi(MethodResource, Resource):
    __state: State = None

    # ------------------------------------------------------------------------
    def __init__(self, state: State = None):
        self.__state = state

    @doc(description="Execute app and get response", tags=["Execution"])
    @use_kwargs(InputSchema, location='json')
    @marshal_with(OutputSchema)  # marshalling
    def post(self, *args) -> OutputClass:
        sid = uuid.uuid4().hex
        data = InputSchema().dump(list(args) if InputSchema().many is True else args[0])
        qid = foreground.prepare(data, sid=sid, state=self.__state)
        return foreground.process(qid)
