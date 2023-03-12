from flask_sqlalchemy import SQLAlchemy
from database.models import Roles

db = SQLAlchemy()


def get_role_by_id(role_id):
    role = Roles.query.get_or_404(role_id)
    return role


def get_roles_from_db():
    return Roles.query.all()


def get_role_by_name(name):
    return Roles.query.filter_by(name=name).first()


def get_role_by_name_or_404(name):
    return Roles.query.filter_by(name=name).first_or_404()


def create_role_in_db(data):
    role = Roles(**data)
    db.session.add(role)
    db.session.commit()
    return role


def delete_role_by_id(role_id):
    role = get_role_by_id(role_id)
    db.session.delete(role)
    db.session.commit()


def change_role_by_id(data, role_id):
    role = get_role_by_id(role_id)
    role.name = data['name']
    role.description = data['description']
    db.session.commit()
    return role
