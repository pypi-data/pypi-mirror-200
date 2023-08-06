import logging
import pathlib
import traceback

from flask import Flask, app, render_template
from flask_cors import CORS

from openfabric_pysdk.config import manifest
from openfabric_pysdk.application import Application
from openfabric_pysdk.context import StateStatus

FlaskApp = Flask(__name__, template_folder=f"{pathlib.Path(__file__).parent}/templates")
CORS(FlaskApp)


@FlaskApp.route("/")
def index():
    return render_template("index.html", manifest=manifest.all())


class Starter:

    @staticmethod
    def ignite(debug, host, port=5000):
        # Setup logger
        logger = logging.getLogger()
        if debug is True:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            logging.getLogger('socketio').setLevel(logging.ERROR)
            logging.getLogger('engineio').setLevel(logging.ERROR)
        application = Application(FlaskApp)
        application.state.status = StateStatus.STARTING

        try:
            # Setup socket services
            application.install_execution_socket('/app')
            # Setup reset services
            application.install_execution_rest('/app')
            application.install_config_rest('/config')
            application.install_specs__rest('/swagger')
            application.install_manifest_rest('/manifest')
            application.install_benchmark_rest('/benchmark')
            application.install_execution_queue('/queue')
            # Install configuration
            application.install_configuration()
            application.state.status = StateStatus.RUNNING
            # Run
            application.run(debug=debug, host=host, port=port)
        except:
            application.state.status = StateStatus.CRASHED
            logging.error(f"Openfabric - failed starting app")
            traceback.print_exc()
