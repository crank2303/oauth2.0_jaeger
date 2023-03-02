from http import HTTPStatus

from flask import jsonify, request, make_response

from database.models import Roles, Users
from database.service import get_roles_by_user, assign_role_to_user, detach_role_from_user
from roles.administrator import required


@required(role='admin')
def users_roles():
    username = request.json.get("username", None)
    if not username:
        return make_response('Username is empty', HTTPStatus.UNAUTHORIZED)
    users_roles = get_roles_by_user(username)
    output = [role.name for role in users_roles]
    return jsonify(roles=output)


@required(role='admin')
def assign_role():
    username = request.json.get("username", None)
    role = request.json.get("role", None)
    if not role or not username:
        return make_response('Role or username is empty', HTTPStatus.UNAUTHORIZED)
    db_role = Roles.query.filter_by(name=role).first()
    if not db_role:
        return make_response('Role does not exist', HTTPStatus.CONFLICT)
    user_db = Users.query.filter_by(login=username).first()
    if not user_db:
        return make_response('User does not exist', HTTPStatus.CONFLICT)
    assign_role_to_user(user_db, db_role)
    return jsonify(msg=f'Role {role} was assigned to user {username}')


@required(role='admin')
def detach_role():
    username = request.json.get('username', None)
    role = request.json.get('role', None)
    if not role or not username:
        return make_response('Role or username is empty', HTTPStatus.UNAUTHORIZED)
    db_role = Roles.query.filter_by(name=role).first()
    if not db_role:
        return make_response('Role does not exist', HTTPStatus.CONFLICT)
    user_db = Users.query.filter_by(login=username).first()
    if not user_db:
        return make_response('User does not exist', HTTPStatus.CONFLICT)
    detach_role_from_user(user_db, db_role)
    return jsonify(msg=f'Role {role} was  detached from user {username}')
