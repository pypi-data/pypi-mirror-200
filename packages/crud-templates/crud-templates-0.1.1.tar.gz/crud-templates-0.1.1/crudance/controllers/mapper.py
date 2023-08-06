from datetime import datetime
from logging import getLogger
from typing import Any, Union

from sqlalchemy import Table, and_
from sqlalchemy.orm import Session, Query

from ..helpers.within_transaction import within_transaction
from ..helpers.exceptions import MissingIdentifyingField, EntityNotFound
from .tools import PostSearchTemplateTools


class InsertMapperTemplate(PostSearchTemplateTools):
    """Template for PUT and PATCH controllers that insert, update or replace entities.

    This controller is to be used when a single table is updated. For replacements
    and updates, one or more columns must allow to uniquely identify the target entity.
    All write operations are wrapped in a nested SQLAlchemy query that will be
    rollbacked in case of an exception.

    :param target: A table's model from SQLAlchemy models to update
    :param session: SQLAlchemy session

    Usage
    =====

    In its simplest form, you just have to init the template with the right target
    table, define the required attribute ``IDENTIFYING_FIELDS``, then use ``put(...)``
    or ``patch(...)`` method. See details below ::

        class MyPutPatchController(InsertMapperTemplate):
            IDENTIFYING_FIELDS = ["id"]

            def __init__(self) -> None:
                super().__init__(target=Persons, session=<sqlalchemy_session>)

    From there, if you want to create a new person ::

        controller = MyPutPatchController()
        created_id = controller.put(body={"firstname": "John", "lastname": "Doe"})

    This will add a new "John Doe" row in the target ``Persons`` table, and return
    the created ``id`` value as a scalar (or a dictionary if there are several
    identifiers).

    If you want to replace the entity, add the id within the input body (and there
    will be no return value) ::

        controller = MyPutPatchController()
        controller.put(body={"id": 1, "firstname": "John", "lastname": "Doe"})

    If you want to update the entity, provide the identifiers and the fields to
    be updated ::

        controller = MyPutPatchController()
        controller.patch(body={"id": 1, "firstname": "Mike"})

    How it works
    ------------

    Whether you want to create or update / replace an entity, the controller first
    tries to find the target in the database from the identifying fields within the
    input body, then triggers the appropriate update behaviour depending on the
    calling method (PUT or PATCH) and on the existence of the entity in database.

    Note that no verification is made that all the fields provided in the input
    body match the columns in the target table. It is advised to check the input
    body beforehand, for instance with a dedicated json schema, to ensure that
    all needed fields are provided with the right type.

    This is especially true for ``put(...)`` calls where you need to ensure that
    all required fields are provided.

    For replacements or updates, if the target table contains an ``updated_at``
    column, it will be updated with the current timestamp.

    Entity existence detection
    --------------------------

    Before attempting the creation / update operation on the database, the controller
    will reach for the ``IDENTIFYING_FIELDS`` key-values pairs within the input
    body, and search for the corresponding entity in the database. The following
    behaviours can occur, that will be appropriately handled by ``put()`` and
    ``patch()`` method afterwards :

    * all identifying fields are provided in the input body but the corresponding
      entity is not found in the database : raise ``EntityNotFound``
    * some of the ``IDENTIYFING_FIELDS`` are missing from the input body, thus
      preventing to look for it in the database : raise ``MissingIdentifyingField``
    * all identifying fields are provided and the entity exists : return the
      premise of the entity as a SQLAlchemy filtering query.

    Entity creation
    ---------------

    Entity creation is made using the ``put(...)`` method. In the case, the input
    body should not contain any of the defined ``IDENTIYFING_FIELDS``, so that an
    SQLAlchemy creation statement will be triggered.

    Once the entity was created, the identifying fields (newly created) are
    returned by the ``put(...)`` call. If there is a single identifying field
    (usually ``id``), it is returned as a scalar, otherwise identifiers are
    returned as a dictionary.

    Entity replacement
    ------------------

    To replace an entity entirely (``PUT`` replacement), the input body must simply
    contain the identifying fields on top of the other fields, for the controller
    to be able to find the target in the database before replacing it. In that
    case the ``put(...)`` method returns nothing, since you're already in posession
    of the identifiers from the input body.

    Note that the identifiers themselves are not updated since they're used to
    target the entity. If you want to write an entity including identifiers,
    you need to set ``IDENTIYFING_FIELDS`` to an empty list, which will trigger
    an entity creation where the whole input body can be written.

    Entity update
    -------------

    To update some fields in an existing entity (``PATCH`` update), the ``patch(...)``
    method behaves roughly the same as the ``put(...)`` except it does not tolerate
    missing identifiers from the input body, and raises ``MissingIdentifyingField``
    or ``EntityNotFound``.

    As for an entity's replacement, the method returns nothing since identifiers
    would already be provided in the input body.

    If you want to update one of the identifiers, you must set ``IDENTIFYING_FIELDS``
    to some other columns that will allow to still uniquely identify the row, then
    run a regular patch. Set the attribute back to real identifiers to avoid unwanted
    identifying behaviour for other regular calls to come afterwards ::

        class MyPutPatchController(InsertMapperTemplate):
            IDENTIFYING_FIELDS = ["id"]  # true identifying fields

            def __init__(self) -> None:
                super().__init__(target=Persons, session=<sqlalchemy_session>)

            def patch_identifiers(self, body: dict) -> None:
                # Change identifying fields and reset them afterwards
                self.IDENTIFYING_FIELDS = ["firstname", "lastname"]
                # Body will contain the new identifiers values
                self.patch(body)
                self.IDENTIFYING_FIELDS = ["id"]

        MyPutPatchController().patch_identifiers(
            {
                "firstname": "John", "lastname": "Doe"  # used to identify the row,
                "id": 3   # will be patched
            }
        )

    Customisation
    -------------

    If you need a multi-table creation / update / replacement, you can still rely
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
    * ``_map_new_target`` and ``_map_existing_target`` will control how the input
      body is written into the various tables, you will likely have to rewrite them
      entirely to be able to write different fields to different tables
    """
    IDENTIFYING_FIELDS = []

    def __init__(self, target: Table, session: Session) -> None:
        super().__init__(target=target, session=session)
        self.logger = getLogger(__name__)

    def put(self, body: dict) -> Union[int, str, dict, None]:
        """Write or replace an entity into the target table with given fields and values.

        If the entity already exists it is replaced and ``None`` is returned,
        else the identification values are returned. If those values amount to a
        scalar it is returned as a scalar, otherwise as a dict.
        """
        identifiers = self._build_identifiers(body)
        if not identifiers:
            # Creation case, will return created identificators as a scalar if single
            entity_identification = within_transaction(
                session=self.session,
                func=self._map_new_target
            )(body=body)
        else:
            # Update case, will return None
            target_entity = self._find_target(identifiers=identifiers)
            entity_identification = within_transaction(
                session=self.session,
                func=self._map_existing_target
            )(target_entity, body=body)

        return entity_identification

    def patch(self, body: dict) -> None:
        """Update an entity from the target table with given fields and values.

        * if the target cannot be looked for because of missing identification fields
          in the input, raise ``MissingIdentifyingField``
        * if the target can be identified but is not found in the table, raise ``EntityNotFound``
        """
        identifiers = self._build_identifiers(body)
        if identifiers is None:
            message = f"Identifying fields {self.IDENTIFYING_FIELDS} cannot be missing for a patch {body}"
            self.logger.error(message)
            raise MissingIdentifyingField(message)

        target = self._find_target(identifiers=identifiers)
        within_transaction(
            session=self.session,
            func=self._map_existing_target
        )(target, body=body)

    def _map_new_target(self, body: dict) -> Any:
        """Add the whole input body as a new row in the target table.

        The SQLAlchemy session is flushed so that any default column (including
        identifiers often) can be available.

        The return value is a scalar if ``IDENTIFYING_FIELDS`` contains a single
        column, else a dictionary.
        """
        new_entity = self.target(**body)

        self.session.add(new_entity)
        self.session.flush()

        created_entity = self._build_identifiers_return(new_entity)
        return created_entity

    def _map_existing_target(self, target: Query, body: dict) -> None:
        """Update the target row with the input body.

        Identifiers will not be set, only other fields. If an ``updated_at`` column
        exists in the updated table, it will be set to the current timestamp.
        """
        for field_name, field_value in body.items():
            if field_name in self.IDENTIFYING_FIELDS:
                # We do not update identifying fields
                continue
            target.update({getattr(self.target, field_name): field_value})

        try:
            target.update({getattr(self.target, "updated_at"): datetime.now()})
        except AttributeError:
            pass  # table does not contain an updated at field

    def _build_identifiers(self, body: dict) -> Union[dict, None]:
        """Build identifying fields from input as a filtering dictionary.

        * If some are missing from the input body, raise ``MissingIdentifyingField``
        * If all are missing from the input body, we assume it is a creation case so
          we just return nothing

        This method can be supercharged or rewritten to build a complex filtering
        dictionary that will be handled with the same logic as the filters from the
        ``PostSearchControllerTemplate``.
        """
        fields = {
            field: body.get(field)
            for field in self.IDENTIFYING_FIELDS
        }

        if not any(fields.values()):
            self.logger.debug(
                "No identifying fields %s found at all, map new target for %s.",
                self.IDENTIFYING_FIELDS, body
            )
            return
        elif not all(fields.values()):
            message = f"Missing one or more identifying fields amongst {self.IDENTIFYING_FIELDS} : {body}"
            self.logger.error(message)
            raise MissingIdentifyingField(message)

        return fields

    def _find_target(self, identifiers: Union[dict, None]) -> Query:
        """Use the identifiers to find the target entity in the database.

        * if found, the entity is returned as a SQLAlchemy query that can then by
          fetched, updated, etc. depending on the calling context
        * if several entites are found a native SQLAlchemy ``MultipleResultsFound``
          is raised
        * if not found, raise ``EntityNotFound``

        In regular cases, ``identifiers`` contains key-value pairs of id columns.
        It can be a whole filtering dictionary for complex cases that will work
        with the same logic as the ``PostSearchControllerTemplate`` filters.
        """
        criteria = self._prepare_filter_criteria(target=self.target, filters=identifiers)
        partial_query = self._init_partial_query()
        target = partial_query.filter(and_(*criteria))

        if target.one_or_none() is None:
            message = f"Entity identified by {identifiers} not found in database !"
            self.logger.error(message)
            raise EntityNotFound(message)

        return target

    def _build_identifiers_return(self, entity: Table) -> Union[int, str, dict]:
        """Build the identifiers from a found or created row in the database.

        If ``IDENTIFYING_FIELDS`` contains only one colum, return the column value
        as a scalar, otherwise return a dictionary.
        """
        fields = {
            field: getattr(entity, field)
            for field in self.IDENTIFYING_FIELDS
        }
        if len(fields.keys()) == 1:
            response = list(fields.values()).pop()
        else:
            response = fields
        return response
