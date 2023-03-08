from datetime import timedelta

import click
from flask import Flask
from flask import send_from_directory
from flask.cli import with_appcontext
from flask_jwt_extended import JWTManager
from flask_redoc import Redoc
from flask_swagger_ui import get_swaggerui_blueprint

import core.logger as logger
from api.v1.blueprint import blueprint
from core.settings import settings
from database.models import Roles
from database.service import create_user, assign_role_to_user


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
    
    @app.route('/static/<path:path>')
    def send_static(path):
        return send_from_directory('static', path)
    
    return app


def app_run():
    app = create_app()
    app.app_context().push()
    return app


if __name__ == "__main__":
    app_run()
