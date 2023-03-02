from flask import Blueprint

from .account import sign_up, login, logout, refresh, login_history, \
    change_login, change_password
from .roles import create_role, delete_role, change_role, roles_list
from .users_roles import users_roles, assign_role, detach_role

blueprint = Blueprint("api/v1", __name__)

blueprint.add_url_rule(
    '/create_role',
    methods=["POST"],
    view_func=create_role,
)
blueprint.add_url_rule(
    '/delete_role',
    methods=["DELETE"],
    view_func=delete_role,
)
blueprint.add_url_rule(
    '/change_role',
    methods=["PUT"],
    view_func=change_role,
)
blueprint.add_url_rule(
    '/roles_list',
    methods=["GET"],
    view_func=roles_list,
)

blueprint.add_url_rule(
    '/users_roles',
    methods=["GET"],
    view_func=users_roles,
)
blueprint.add_url_rule(
    '/assign_role',
    methods=["POST"],
    view_func=assign_role,
)
blueprint.add_url_rule(
    '/detach_role',
    methods=["DELETE"],
    view_func=detach_role,
)

blueprint.add_url_rule(
    '/change_login',
    methods=["POST"],
    view_func=change_login,
)
blueprint.add_url_rule(
    '/change_password',
    methods=["POST"],
    view_func=change_password,
)
blueprint.add_url_rule(
    '/login',
    methods=["POST"],
    view_func=login,
)
blueprint.add_url_rule(
    '/login_history',
    methods=["GET"],
    view_func=login_history,
)
blueprint.add_url_rule(
    '/logout',
    methods=["DELETE"],
    view_func=logout,
)
blueprint.add_url_rule(
    '/refresh',
    methods=["GET"],
    view_func=refresh,
)
blueprint.add_url_rule(
    '/sign_up',
    methods=["POST"],
    view_func=sign_up,
)
