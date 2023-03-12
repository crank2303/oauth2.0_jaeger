
import click

from datetime import timedelta
from flask import Flask, json
from flask import request, send_from_directory

from flask.cli import with_appcontext
from flask_jwt_extended import JWTManager
from flask_redoc import Redoc
from flask_swagger_ui import get_swaggerui_blueprint
from werkzeug.exceptions import HTTPException
from opentelemetry.instrumentation.flask import FlaskInstrumentor

import core.logger as logger
from api.v1.blueprint import blueprint
from core.settings import settings

from core.limiters import limiter
from core.oauth import init_oauth
from database.models import Roles
from database.service import create_user, assign_role_to_user
from core.tracers import configure_tracer
from api.v1.oauth import oauth_route


ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
REFRESH_TOKEN_EXPIRES = timedelta(days=7)

app = Flask(__name__)

app.config['REDOC'] = {
    'spec_route': '/docs',
    'title': 'Flask Auth Service', }

redoc = Redoc(app, 'service.yml')

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger_config.yml'
swagger_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Auth service API documentation',
    },
)


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


if settings.enable_tracer:
    @app.before_request
    def before_request():
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            raise RuntimeError('request id is required')

    # Конфигурируем и добавляем трейсер
    configure_tracer()
    FlaskInstrumentor().instrument_app(app)


@click.command(name='create-superuser')
@with_appcontext
def create_superuser():
    superuser = create_user(
        username=settings.admin_username,
        password=settings.admin_password)
    role = Roles.query.filter_by(name='admin').first()
    if superuser and role:
        assign_role_to_user(superuser, role)
        logger.save_log.info(msg='Superuser was created')
    else:
        logger.save_log.error(msg='Error while creating superuser')


def create_app():
    app.config["JWT_SECRET_KEY"] = settings.jwt_secret_key
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ACCESS_TOKEN_EXPIRES
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = REFRESH_TOKEN_EXPIRES

    app.cli.add_command(create_superuser)

    app.register_blueprint(swagger_blueprint)
    app.register_blueprint(blueprint, url_prefix='/api/v1')

    JWTManager(app)

    if settings.enable_limiter:
        limiter.init_app(app)

    init_oauth(app)

    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)

    api_v1 = '/api/v1'
    app.register_blueprint(oauth_route, url_prefix=f'{api_v1}/oauth')

    return app


def app_run():
    app = create_app()
    app.app_context().push()
    return app


if __name__ == "__main__":
    app.run(debug=settings.flask_debug)
