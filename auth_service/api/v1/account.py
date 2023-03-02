from datetime import timedelta
from http import HTTPStatus

from flask import jsonify, request, make_response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jti, get_jwt
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from werkzeug.security import check_password_hash, generate_password_hash

from database.cache_redis import redis_app
from database.models import Users, AuthLogs
from database.service import auth_log, create_user, change_password, change_username

ACCESS_EXPIRES = timedelta(hours=1)
REFRESH_EXPIRES = timedelta(days=30)

storage = redis_app


def sign_up():
    username = request.values.get("email", None)
    password = request.values.get("password", None)
    if not username or not password:
        return make_response('email or password are empty!', HTTPStatus.UNAUTHORIZED,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = Users.query.filter_by(login=username).first()
    if user:
        return make_response('Email has already registered!', HTTPStatus.UNAUTHORIZED,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})

    new_user = create_user(username, password)

    access_token = create_access_token(identity=new_user.id, fresh=True)
    refresh_token = create_refresh_token(identity=new_user.id)
    user_agent = request.headers['user_agent']

    auth_log(user=new_user, user_agent=user_agent, ip_address=request.remote_addr, log_type=request.user_agent.browser)

    key = ':'.join(('user_refresh', user_agent, get_jti(refresh_token)))
    storage.set(key, str(new_user.id), ex=REFRESH_EXPIRES)

    return jsonify(access_token=access_token,
                   refresh_token=refresh_token)


def login():

    auth = request.authorization

    if not auth.username or not auth.password:
        return make_response('Email or password are empty!', HTTPStatus.UNAUTHORIZED,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = Users.query.filter_by(login=auth.username).first()
    if not user:
        return make_response('Username does not exist!', HTTPStatus.UNAUTHORIZED,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(identity=user.id)
        user_agent = request.headers['user_agent']

        auth_log(user=user, user_agent=user_agent, ip_address=request.remote_addr, log_type=request.user_agent.browser)

        key = ':'.join(('user_refresh', user_agent, get_jti(refresh_token)))
        storage.set(key, str(user.id), ex=REFRESH_EXPIRES)

        return jsonify(access_token=access_token,
                       refresh_token=refresh_token)

    return make_response('Password is incorrect!', HTTPStatus.UNAUTHORIZED,
                         {'WWW-Authenticate': 'Basic realm="Login required!"'})


@jwt_required(verify_type=False)
def logout():
    token = get_jwt()
    jti = token["jti"]
    ttype = token["type"]
    user_agent = request.headers['user_agent']
    key = ':'.join((jti, user_agent))
    redis_app.set(key, "", ex=ACCESS_EXPIRES)

    return jsonify(msg=f"{ttype.capitalize()} token successfully revoked")


@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    token = get_jwt()
    jti = token["jti"]
    user_agent = request.headers['user_agent']
    key = ':'.join(('user_refresh', user_agent, jti))
    user_db = storage.get(key).decode('utf-8')
    if identity == user_db:
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        # запись в Redis refresh token
        key = ':'.join(('user_refresh', user_agent, get_jti(refresh_token)))
        storage.set(key, identity, ex=REFRESH_EXPIRES)

        return jsonify(access_token=access_token,
                       refresh_token=refresh_token)

    return make_response('Could not verify', HTTPStatus.UNAUTHORIZED,
                         {'WWW-Authenticate': 'Basic realm="Login required!"'})


@jwt_required()
def login_history():
    user_id = get_jwt_identity()

    history = AuthLogs.query.filter_by(user_id=user_id). \
        order_by(AuthLogs.auth_date.desc()). \
        limit(10)
    output = []
    for record in history:
        record_data = {'user_agent': record.user_agent,
                       'auth_date': record.auth_date}
        output.append(record_data)
    return jsonify(login_history=output)


@jwt_required()
def change_login():

    new_username = request.values.get('new_username')
    user = Users.query.filter_by(login=new_username).first()
    if user:
        return make_response('Login already existed', HTTPStatus.BAD_REQUEST)

    identity = get_jwt_identity()
    current_user = Users.query.filter_by(id=identity).first()
    change_username(user=current_user, new_login=new_username)

    return jsonify(msg='Login successfully changed')


@jwt_required()
def change_password():

    new_password = request.values.get('new_password')

    identity = get_jwt_identity()
    current_user = Users.query.filter_by(id=identity).first()
    change_password(current_user, new_password)

    access_token = create_access_token(identity=identity, fresh=True)
    refresh_token = create_refresh_token(identity=identity)
    user_agent = request.headers['user_agent']

    # запись в Redis refresh token
    key = ':'.join(('user_refresh', user_agent, get_jti(refresh_token)))
    storage.set(key, str(identity), ex=REFRESH_EXPIRES)

    return jsonify(msg='Password successfully changed',
                   access_token=access_token,
                   refresh_token=refresh_token)
