import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .postgresql import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    login = Column(
        String(30),
        unique=True,
        nullable=False,
    )
    password = Column(
        String(30),
        nullable=False,
    )
    authlogs = relationship(
        "AuthLogs",
        back_populates="user",
        cascade="all, delete",
        passive_deletes=True,
    )
    def __repr__(self):
        return f'<User {self.login}>'


class AuthLogs(Base):
    __tablename__ = 'auth_logs'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Users.id, ondelete="CASCADE"),
        nullable=False,
    )
    user_agent = Column(
        String(30),
        nullable=False,
    )
    log_type = Column(
        String(30),
        nullable=True,
    )
    datetime = Column(
        DateTime,
        nullable=False,
        default=datetime.now()
    )
    ip_address = Column(
        String(30),
        nullable=True,
    )
    user = relationship(
        "Users",
        back_populates="authlogs",
    )


class Roles(Base):
    __tablename__ = 'roles'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    name = Column(
        String(30),
        unique=True,
        nullable=False,
    )

    def __repr__(self):
        return f'<Roles {self.name}>'


class UsersRoles(Base):
    __tablename__ = 'users_roles'

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Users.id),
    )
    role_id = Column(
        UUID(as_uuid=True),
        ForeignKey(Roles.id),
    )
