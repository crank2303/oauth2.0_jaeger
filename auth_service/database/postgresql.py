from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from core.settings import settings

SQLALCHEMY_DATABASE_URI = f'postgresql://{settings.postgres_user}:{settings.postgres_password}@' \
                          f'{settings.pg_host}:{settings.pg_port}/{settings.postgres_db}'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()

Base.query = db_session.query_property()
