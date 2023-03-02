import uuid
from typing import List

from werkzeug.security import generate_password_hash

from .models import Users, AuthLogs, Roles, UsersRoles
from .postgresql import db


def create_user(username, password):
    hashed_password = generate_password_hash(password, method='sha256')
    new_user = Users(login=username,
                     password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return new_user


def get_user(username: str) -> Users:
    user = Users.query.filter_by(username=username).first()
    return user


def auth_log(user: Users, user_agent: str, ip_address: str, log_type: str):
    new_session = AuthLogs(user_id=user.id,
                           user_agent=user_agent,
                           log_type=log_type,
                           ip_address=ip_address,
                           )
    db.session.add(new_session)
    db.session.commit()


def get_users_roles(user_id: uuid) -> List[Roles]:
    users_roles = UsersRoles.query.filter_by(user_id=user_id).all()
    if not users_roles:
        return []
    output = []
    for role in users_roles:
        role = Roles.query.filter_by(id=role.role_id).first()
        output.append(role)
    return output


def change_username(user: Users, username: str):
    user.username = username
    db.session.commit()


def change_password(user: Users, password: str):
    hashed_password = generate_password_hash(password, method='sha256')
    user.password = hashed_password
    db.session.commit()


def create_role_db(role_name: str) -> Roles:
    new_role = Roles(name=role_name)
    db.session.add(new_role)
    db.session.commit()

    return new_role


def delete_role_db(role: Roles):
    db.session.delete(role)
    db.session.commit()


def change_role_db(role_name: str, new_name: str):
    role = Roles.query.filter_by(name=role_name).first()
    role.name = new_name
    db.session.commit()


def get_roles_by_user(username: str) -> List[Roles]:
    user = Users.query.filter_by(username=username).first()
    roles = UsersRoles.query.filter_by(user_id=user.id).all()
    output = []
    for role in roles:
        role = Roles.query.filter_by(id=role.role_id).first()
        output.append(role)
    return output


def assign_role_to_user(user: Users, role: Roles):
    new_assignment = UsersRoles(user_id=user.id,
                                role_id=role.id)
    db.session.add(new_assignment)
    db.session.commit()


def detach_role_from_user(user: Users, role: Roles):
    db.session.query(UsersRoles).filter_by(user_id=user.id,
                                           role_id=role.id).delete()
    db.session.commit()

