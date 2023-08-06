from functools import wraps
from typing import Callable

from sqlalchemy.orm import Session


def within_transaction(session: Session, func: Callable) -> Callable:
    """Wrap a function call around a nested sqlalchemy session commit or rollback.

    :param session: SQLAlchemy seession to nest if needed
    :param func: function to execute in the session context with rollback behaviour

    The method can be used a decorator. In ``crudance`` it is used in the simple
    functional form to allow using a dynamic ``session`` argument::

        within_transaction(fun)(*args, **kwargs)
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.is_active:
            session.begin_nested()
        else:
            session.begin()

        try:
            result = func(*args, **kwargs)
            session.commit()
            return result
        except Exception:
            session.rollback()
            raise

    return wrapper
