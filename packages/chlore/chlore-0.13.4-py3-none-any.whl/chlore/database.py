import sqlalchemy
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql.elements import BinaryExpression
from functools import cache
from fastapi import Depends

from chlore.config import CONFIG


class DatabaseSession(Session):
    pass


@cache
def get_engine():
    if CONFIG.database is None:
        raise ConfigurationError("Chlore: SQL Engine cannot be used without a config entry.")
    return sqlalchemy.create_engine(CONFIG.database.url)


@cache
def get_session_maker():
    engine = get_engine()
    return sessionmaker(engine, class_=DatabaseSession)


def session() -> DatabaseSession:
    """
    FastAPI dependency to acquire the database handle. For elegance, one should
    not import this directly into it's namespace, but rather import the module
    and write `Depends(database.session)`.
    """
    session_maker = get_session_maker()
    with session_maker() as session:
        yield session
