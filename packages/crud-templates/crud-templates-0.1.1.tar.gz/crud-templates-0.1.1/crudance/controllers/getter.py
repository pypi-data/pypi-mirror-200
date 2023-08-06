from logging import getLogger

from sqlalchemy import Table
from sqlalchemy.orm import Query, Session
from sqlalchemy.exc import MultipleResultsFound

from ..helpers.within_transaction import within_transaction
from ..helpers.exceptions import MissingIdentifyingField, EntityNotFound
from .mapper import InsertMapperTemplate


class GetterDeleterTemplate(InsertMapperTemplate):
    """Template for GET and DELETE controllers.

    This controller is to be used when a single table is queried from the database
    with one or more columns that can uniquely identify the target entity.

    :param target: A table's model from SQLAlchemy models to search elements into
    :param session: SQLAlchemy session

    Usage
    =====

    In its simplest form, you just have to init the template with the right target
    table, define the required attributes ``IDENTIFYING_FIELDS`` and ``TARGET_FIELDS``,
    then use ``get(...)`` or ``delete(...)`` method. See details below.

    The controller inherits from the ``InsertMapperTemplate`` to use the methods
    that identify a target from a set of identifying fields, and are able to trigger
    a ``NotFoundEntity`` or ``MissingIdentifyingField``.

    Get and serialise an element
    ----------------------------

    A simple ``GET`` needs the following parameters : a target table, a set of
    columns that allows to identify the entity, and the target fields to serialise
    to the output.

    * the target table is given at instanciation
    * the identifying columns names are given in ``IDENTIFYING_FIELDS`` attribute
    * the columns to keep for serialisation are given in ``TARGET_FIELDS``. If
      some of them are dates, you can serialise them as isoformat strings by
      setting them in ``DATE_FIELDS`` attribute.

    Note that by default ``TARGET_FIELDS`` is empty, so you have to write them
    precisely otherwise nothing will be returned even if the entity is found.

    In most cases there's a single identifying columns but it works the same as
    if there are several. Here's an exemple of a working controller that gets an
    entity using two identifying fields, and serialises a date among other fields::

        class MySuperGetter(GetterDeleterTemplate):
            IDENTIFYING_FIELDS = ["firstname", "lastname"]
            TARGET_FIELDS = ["id", "firstname", "lastname", "birthday", "gender"]
            DATE_FIELDS = ["birthday"]

            def __init__(self) -> None:
                super().__init__(target=Persons, session=<sqlalchemy_session>)

    From there, in the GET service, you just have to do the following::

        getter = MySuperGetter()
        serialised_person = getter.get(firstname="John", lastname="Doe")

    The response would be of the form::

        {
            "id": 1,
            "firstname": "John",
            "lastname": "Doe",
            "birthday": "1998-07-12",
            "gender": "male"
        }

    If the entity is not found, an ``EntityNotFound`` is raised. If some of the
    identifying fields are not provided in the input, a ``MissingIdentifyingField``
    is raised.

    Delete an element
    -----------------

    A DELETE controller would work very much like the GET controller except that
    there is no serialisation nor returned value.

    The deletion query is encapsulated in a nested SQLAlchemy transaction that will
    be rollbacked in the following two cases :

    * there was no entity found from the identifiers, raises ``EntityNotFound``
    * there would be several entities to delete given the identifiers, raises
      ``sqlalchemy.exc.MultipleResultsFound``

    Continuing from the previous example, we could set a DELETE controller as::

        delete_controller = MySuperGetter()
        delete_controller.delete(firstname="John", lastname="Doe")

    Customisation
    -------------

    If you need a multi-table query or a nested serialisation, you can still rely
    on the parent's class methods to avoid rewriting the whole controller, by
    using the filtering logic of its methods.

    Here are the methods that you might want to supercharge or rewrite to allow
    querying from several tables :

    * ``_build_identifiers`` should return the filters that would allow to retrieve
      the entity from the table(s). This is the same filter structure as the one
      ``PostSearchControllerTemplate`` uses, see there for details.
    * ``_find_target`` executes the filtering query from the identifiers previously
      built. If querying a single table you might not need to change it, but
      if several tables you have to expand the query to those tables by rewriting
      the method
    * ``_serialize`` by default looks only for columns from ``TARGET_FIELDS``
      and attempt a flat serialization (apart from dates). Since any missing field
      is passed, you can give a minimal set of regular ``TARGET_FIELDS`` then
      supercharge the method for more advanced serialisation
    """
    TARGET_FIELDS = []  # Fields to serialize from found entity

    def __init__(self, target: Table, session: Session) -> None:
        super().__init__(target, session)
        self.logger = getLogger(__name__)

    def get(self, **ids) -> dict:
        """Find a uniquely identified entity and serialize according to target fields.

        Identifying fields must be given as keywords argument to allow building
        a filtering dictionary to find the entity through an SQLAlchemy query.

        Most of the time the only field will be ``id`` so the call would
        actually be ``get(self, id=<target-id>)``.
        """
        target = self._identify_target(body=ids).first()  # NotFound is already handled
        response = self._serialize(element=target, selected_fields=self.TARGET_FIELDS)
        return response

    def delete(self, **ids) -> None:
        """Delete a uniquely identified entity with rollback tolerance.

        Identifying fields must be given as keywords argument to allow building
        a filtering dictionary to find the entity through an SQLAlchemy query.

        Most of the time the only field will be ``id`` so the call would
        actually be ``delete(self, id=<target-id>)``.
        """
        target_query = self._identify_target(body=ids)
        within_transaction(
            session=self.session,
            func=self._execute_delete
        )(body=ids, query=target_query)

    def _identify_target(self, body: dict) -> Query:
        """Build a filtering query to get the target identified from the parameters.

        If any (or all) of ``IDENTIFYING_FIELDS`` is missing within the body,
        raise ``MissingIdentifyingField`.`

        :param body: All keywords parameters of the parent calling method
        :return: SQLAlchemy query that can then be updated, yielded, etc.
        """
        identifiers = self._build_identifiers(body)
        if identifiers is None:
            message = f"Identifying fields {self.IDENTIFYING_FIELDS} are compulsory for GET : {body}"
            self.logger.error(message)
            raise MissingIdentifyingField(message)

        return self._find_target(identifiers=identifiers)

    def _execute_delete(self, body: dict, query: Query) -> None:
        """Execute the deletion query and raise according to the result.

        * If no row was deleted, raise ``EntityNotFound``
        * If several were deleted, raise ``sqlalchemy.exc.MultipleResultsFound``
        """
        deleted_count = query.delete()
        if deleted_count < 1:
            message = f"Impossible to delete not found entity {body}"
            self.logger.error(message)
            raise EntityNotFound(message)
        elif deleted_count > 1:
            message = f"Several rows would be deleted from DELETE with {body}, rollback."
            self.logger.error(message)
            raise MultipleResultsFound(message)
