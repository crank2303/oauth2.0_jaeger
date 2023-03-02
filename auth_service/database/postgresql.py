# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.settings import settings

# db = SQLAlchemy()

SQLALCHEMY_DATABASE_URI = f'postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.pg_host}:{settings.pg_port}/{settings.postgres_db}'


engine = create_engine(SQLALCHEMY_DATABASE_URI)

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# def init_db(app: Flask):
#     app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#     db.init_app(app)
    
