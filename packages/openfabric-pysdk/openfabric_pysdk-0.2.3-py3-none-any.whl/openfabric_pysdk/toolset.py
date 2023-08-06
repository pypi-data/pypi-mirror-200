from typing import List, Union
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource
from marshmallow import fields, Schema, post_load
from webargs.flaskparser import use_args
from openfabric_pysdk import benchmark
from openfabric_pysdk.config import manifest, state_config
from openfabric_pysdk.context import State
from openfabric_pysdk.loader import *
from openfabric_pysdk.utility import SchemaUtil


#######################################################
#  Config API
#######################################################

class UserIdClass(Schema):
    uid: str = None


class UserIdSchema(Schema):
    uid = fields.String(required=True)

    @post_load
    def create(self, data, **kwargs):
        return SchemaUtil.create(UserIdClass(), data)


class ConfigRestApi(MethodResource, Resource):
    __state: State = None

    # ------------------------------------------------------------------------
    def __init__(self, state: State = None):
        self.__state = state

    @doc(description="Get APP configuration", tags=["Developer"])
    @use_args(UserIdSchema, location='query')
    @marshal_with(ConfigSchema)
    def get(self, uidc: UserIdClass) -> ConfigClass:
        with MeasureBlockTime("ConfigRestApi::get"):
            config = state_config.get(uidc.uid)
            if config is False:
                return dict()
            return config

    @doc(description="Set APP configuration", tags=["Developer"])
    @use_args(UserIdSchema, location='query')
    @use_args(ConfigSchema, location='json')
    @marshal_with(ConfigSchema)
    def post(self, uidc: UserIdClass, config: Union[ConfigClass, List[ConfigClass]]) -> ConfigClass:

        with MeasureBlockTime("ConfigRestApi::post"):
            if ConfigSchema().many is True:
                config = list(config)
            else:
                config = config[0] if type(config) == list else config
            state_config.set(uidc.uid, ConfigSchema().dump(config))
            if config_callback_function:
                config = dict(map(lambda kv: (kv[0], ConfigSchema().load(kv[1])), state_config.all().items()))
                config_callback_function(config, self.__state)
            return config


#######################################################
#  Manifest API
#######################################################
class ManifestSchema(Schema):
    name = fields.String(description="App name")
    version = fields.String(description="App version")
    description = fields.String(description="APP description")
    organization = fields.String(description="APP organization")
    sdk = fields.String(description="APP sdk")
    overview = fields.String(description="APP overview")
    input = fields.String(description="APP input")
    output = fields.String(description="APP output")

    def __init__(self):
        super().__init__(many=False)


class ManifestRestApi(MethodResource, Resource):

    @doc(description="Get APP manifest", tags=["Developer"])
    @marshal_with(ManifestSchema)  # marshalling
    def get(self):
        with MeasureBlockTime("ManifestRestApi::get"):
            return manifest.all()


#######################################################
#  Benchmark API
#######################################################
class BenchmarkSchema(Schema):
    name = fields.String()
    avg = fields.String()
    count = fields.String()
    stddev = fields.String()
    min = fields.String()
    max = fields.String()

    def __init__(self):
        super().__init__(many=True)


class BenchmarkRestApi(MethodResource, Resource):

    @doc(description="Get APP benchmarks", tags=["Developer"])
    @marshal_with(BenchmarkSchema)  # marshalling
    def get(self):
        with MeasureBlockTime("BenchmarkRestApi::get"):
            return benchmark.get_all_timings_json()
