import logging

from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, session
from flask_apispec import FlaskApiSpec
from flask_restful import Api

from openfabric_pysdk.config import manifest, state_config
from openfabric_pysdk.toolset import ConfigRestApi, ManifestRestApi, BenchmarkRestApi
from openfabric_pysdk.transport.queue import *
from openfabric_pysdk.transport.rest import ExecutionRestApi
from openfabric_pysdk.transport.socket import Socket


#######################################################
#  Application
#######################################################
class Application:
    state: State = None
    __api: Api = None
    __app: Flask = None
    __socket: Socket = None
    __docs: FlaskApiSpec = None

    # ------------------------------------------------------------------------
    def __init__(self, app: Flask):
        self.__app = app
        self.__api = Api(app)
        self.__docs = FlaskApiSpec(app)
        self.state = State()

    # ------------------------------------------------------------------------
    def install_specs__rest(self, endpoint):
        logging.info(f"Openfabric - install Specs REST endpoints on {endpoint}")
        specs = {
            'APISPEC_SPEC': APISpec(
                title="App " + manifest.get('name'),
                version=manifest.get('version'),
                plugins=[MarshmallowPlugin()],
                openapi_version='2.0.0',
                info=dict(
                    termsOfService='https://openfabric.ai/terms/',
                    contact=dict(
                        name=manifest.get('organization'),
                        url="https://openfabric.ai"
                    ),
                    description=manifest.get('description')),
            ),
            'APISPEC_SWAGGER_URL': f'/{endpoint}/',  # URI to access API Doc JSON
            'APISPEC_SWAGGER_UI_URL': f'/{endpoint}-ui/'  # URI to access UI of API Doc
        }
        self.__app.config.update(specs)

    # ------------------------------------------------------------------------
    def install_execution_rest(self, endpoint):
        logging.info(f"Openfabric - install Execution REST endpoints on {endpoint}")

        resource_args = dict(state=self.state)

        self.__api.add_resource(ExecutionRestApi, endpoint, resource_class_kwargs=resource_args)
        self.__docs.register(ExecutionRestApi, resource_class_kwargs=resource_args)

    # ------------------------------------------------------------------------
    def install_config_rest(self, endpoint):
        if ConfigSchema is None:
            logging.warning(f"Openfabric - no Config schema available")
            return
        logging.info(f"Openfabric - install Config REST endpoints on {endpoint}")

        resource_args = dict(state=self.state)

        self.__api.add_resource(ConfigRestApi, endpoint, resource_class_kwargs=resource_args)
        self.__docs.register(ConfigRestApi, resource_class_kwargs=resource_args)

    # ------------------------------------------------------------------------
    def install_manifest_rest(self, endpoint):
        logging.info(f"Openfabric - install Manifest REST endpoints on {endpoint}")
        self.__api.add_resource(ManifestRestApi, endpoint)
        self.__docs.register(ManifestRestApi)

    # ------------------------------------------------------------------------
    def install_benchmark_rest(self, endpoint):
        logging.info(f"Openfabric - install Benchmark REST endpoints on {endpoint}")
        self.__api.add_resource(BenchmarkRestApi, endpoint)
        self.__docs.register(BenchmarkRestApi)

    # ------------------------------------------------------------------------
    def install_execution_queue(self, endpoint):
        logging.info(f"Openfabric - install Execution REST Queue endpoints on {endpoint}")

        resource_args = dict(state=self.state)

        self.__api.add_resource(QueueApi_Get, endpoint + "/get", resource_class_kwargs=resource_args)
        self.__docs.register(QueueApi_Get, resource_class_kwargs=resource_args)

        self.__api.add_resource(QueueApi_List, endpoint + "/list", resource_class_kwargs=resource_args)
        self.__docs.register(QueueApi_List, resource_class_kwargs=resource_args)

        self.__api.add_resource(QueueApi_Post, endpoint + "/post", resource_class_kwargs=resource_args)
        self.__docs.register(QueueApi_Post, resource_class_kwargs=resource_args)

        self.__api.add_resource(QueueApi_Delete, endpoint + "/delete", resource_class_kwargs=resource_args)
        self.__docs.register(QueueApi_Delete, resource_class_kwargs=resource_args)

    # ------------------------------------------------------------------------
    def install_execution_socket(self, endpoint):
        logging.info(f"Openfabric - install Execution SOCKET endpoints on {endpoint}")
        self.__socket = Socket(endpoint, session, self.__app, self.state)

    # ------------------------------------------------------------------------
    def install_configuration(self):
        logging.info(f"Openfabric - install APP configuration")
        if config_callback_function:
            items = state_config.all().items()
            config = dict(map(lambda kv: (kv[0], ConfigSchema().load(kv[1])), items))
            if config:
                config_callback_function(config, self.state)

    # ------------------------------------------------------------------------
    def run(self, debug, host, port):
        self.__socket.run(debug=debug, host=host, port=port)
        # self.__app.run(debug=debug, host=host, port=port)
