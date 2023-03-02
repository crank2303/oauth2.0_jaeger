from http import HTTPStatus

from flask import jsonify, request, make_response

from database.models import Roles
from database.service import create_role_db, delete_role_db, change_role_db
from roles.administrator import required


@required(role='manager')
def create_role():
    role = request.values.get('role', None)
    if not role:
        return make_response('New role is empty', HTTPStatus.BAD_REQUEST)
    db_role = Roles.query.filter_by(name=role).first()
    if db_role:
        return make_response('Role is already exist', HTTPStatus.BAD_REQUEST)
    create_role_db(role)
    return jsonify(msg=f'Role {role} was successfully created')


@required(role='manager')
def delete_role():
    role = request.values.get("role", None)
    if not role:
        return make_response('Role is empty',
                             HTTPStatus.BAD_REQUEST)
    db_role = Roles.query.filter_by(name=role).first()
    if not db_role:
        return make_response('Role does not exist',
                             HTTPStatus.NOT_FOUND)
    delete_role_db(db_role)
    return jsonify(msg=f'Role {role} was successfully deleted')


@required(role='manager')
def change_role():
    role = request.values.get("role", None)
    new_role = request.values.get("new_name", None)
    if not role or not new_role:
        return make_response('Role or new name is empty',
                             HTTPStatus.BAD_REQUEST)
    db_role = Roles.query.filter_by(name=role).first()
    if not db_role:
        return make_response('Role does not exist', HTTPStatus.NOT_FOUND)
    change_role_db(role, new_role)
    return jsonify(msg=f'Role {role} was successfully changed')


@required(role='manager')
def roles_list():
    roles = Roles.query.all()
    output = [role.name for role in roles]
    return jsonify(roles=output)
