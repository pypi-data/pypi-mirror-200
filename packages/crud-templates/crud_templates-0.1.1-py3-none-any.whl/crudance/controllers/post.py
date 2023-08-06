from math import ceil
from logging import getLogger
from typing import List, Union, Tuple

from sqlalchemy import and_, or_, desc
from sqlalchemy.orm import Session, Query
from sqlalchemy.schema import Table

from ..config import DEFAULT_PAGE, DEFAULT_PAGE_SIZE
from ..config.fields import PostInputFields
from .tools import PostSearchTemplateTools


class PostSearchControllerTemplate(PostSearchTemplateTools):
    """Template controller for endpoints that search entities from a standardised POST.

    The template provides a simple way to create searching controllers to get
    entities from the database by creating SELECT queries with tailored filters.

    :param target: A table's model from SQLAlchemy models to search elements into
    :param session: SQLAlchemy session

    Usage
    =====

    The input body must abide by the ``PostInputSchema``, which means having
    at least a `filters` (even if empty) field, and a `fields` field giving the
    columns from the target table to return. Since this is a search and not a
    `GET`, returned fields can only be returned from the (main) target table by
    default.

    Querying columns from other tables should be handled in ``GET`` endpoints once
    you got the list of entities you wish to get something from. If you really
    need to serialise from join tables, you have to supercharge at least the
    `_serialize` method to get results from the join table(s) too.

    Simple searches on a single table
    ---------------------------------

    In its simplest form, you don't have anything to write if you just want a
    simple search onto a single table. The searching controller will only have
    to inherit from the template and provide the target table at instanciation::

        class MyController(PostSearchControllerTemplate):

            def __init__(self, session):
                super().__init__(target=MyTable, session=session)

    Calling ``MyController().search(**body)`` will handle querying the table
    (with order if provided), applying the filters, getting the right fields and
    exporting results as a dictionary.

    Querying is made with a default limit (10) and offset (0), and the result is
    of the form::

        {
            "data": [
                { # serialized found element},
                ...
            ],
            "pagination": {
                "items": 12,
                "pages": 1
            }
        }

    Simple search on joined tables
    ------------------------------

    Searching entities by filtering on join tables on top of the target
    table is made through the specification of a join filter and a mapping method
    to know how to join the table to the main query. This is done by defining the
    join filter within ``self.JOINS_FILTER`` as such ::

        {
            "slot": "joined_table",  # name of the nested filter in the input body
            "table": JoinedTable     # target table from the orm
            "map_method": "map_joined_table"  # mapping method for the query
        }

    Then define how to join by writing the mapping method. In most cases it consists
    only in adding one or several joins to the partial. The mapping method must have the
    following signature because it is how it will be called when the controller
    builds the partial query::

        def map_joined_table(self, partial: Query, filters: dict) -> Query:
            return partial.join(JoinedTable)

    You can take advantage of the mapping method to customize precisely how the
    join will work, even applying the filter at that step if needed, without a true
    join::

        def map_joined_table(self, partial: Query, filters: dict) -> Query:
            join_partial_query = self._apply_filters_clause(
                partial=self.session.query(JoinedTable.id),  # use a local query on the join table
                target=JoinedTable,
                filters=filters.pop("joined_table")  # we have to remove it from the filters since it is used here
            )
            join_ids = join_partial_query.all()

            return partial.filter(Table.joined_id.in_(join_ids))

    Range filters can be created for any column of the query (from both main or joined tables),
    provided they :

        * are enlisted in ``self.RANGE_FILTERS``
        * appear as nested dictionaries too in the input body's filters
        * the corresponding table appear in the partial query for joins

    See ``PostSearchTemplateTools`` for details on joins and range filter.

    Customizing
    ===========

    Controlling complex joins
    -------------------------

    The mapping methods defined in ``self.JOINS_FILTERS`` will be called by
    ``_init_partial_query`` only if the corresponding filter (``slot``) is found
    in the input body's filters. If the filter is not asked the join won't happen,
    which allows to keep the queries light when it's not needed to join.

    If the ``map_method`` from the join filter definition in ``self.JOINS_FILTERS``
    does not exist, the join is simply skipped. You can take advantage of this to
    write a single join that relies on several filters, or filters that target
    the same join table(s).

    Repeating the same target table for various ``JOINS_FILTERS`` will actually
    repeat the join which can have desastrous consequences for the query. In that
    case, it is advised to manually write the desired relations between the filters
    and the joins by supercharging ``_init_partial_query`` without defining the
    mapping method in ``JOINS_FILTERS``. For instance if two different filters
    uses the same join from two tables::

        class TailoredController(PostSearchControllerTemplate):
            JOINS_FILTERS = [
                # suppose the following two always need to be both joined for the
                # query and filter to work
                {
                    "slot": "intermediary_table",
                    "table": IntermediaryTable
                },
                {
                    "slot": "other_table",
                    "table": OtherTable
                }
            ]

            def _init_partial_query(self, filters: dict) -> Query:
                # no joins will be added here since the mapping methods were not provided
                # in the join filter definition
                partial = super()._init_partial_query(self, filters)

                # now define a tailored join behaviour
                # here we want the same join for two different filters
                # that can both be present in the input body
                if filters.get("intermediary_table") or filters.get("other_table"):
                    partial = partial.join(IntermediaryTable).join(OtherTable)

                return partial
    """
    def __init__(self, target: Table, session: Session) -> None:
        super().__init__(target=target, session=session)
        self.logger = getLogger(__name__)

    def search(self, **kwargs) -> dict:
        """Do the search after applying filters and return paginated results.

        The input will usually be the input from the endpoint itself, which should
        usually abide by ``PostInputSchema``.

        :return: Paginated results, should abide by ``PostOutputSchema``
        """
        selected_fields = kwargs.get(PostInputFields.fields, [])
        operator = kwargs.get(PostInputFields.operator_choice, PostInputFields.Operators.and_)
        filters = kwargs.get(PostInputFields.filters, {})
        order_by = kwargs.get(PostInputFields.order_by, [])
        pagination = kwargs.get(PostInputFields.pagination, {})

        self.logger.debug("Initialize query on target table %s and joins if needed.", self.target)
        partial = self._init_partial_query(filters)

        self.logger.debug("Apply filtering clauses")
        partial = self._apply_filters_clause(partial, self.target, filters, operator)

        self.logger.debug("Apply order by clause")
        partial = self._apply_order_by_clause(partial, order_by)

        self.logger.debug("Get results")
        results = self._get_page(partial, pagination)

        self.logger.debug("Serialize results")
        response = {
            "data": [self._serialize(element, selected_fields) for element in results]
        }

        if pagination.get(PostInputFields.Pagination.total):
            self.logger.debug("Get total counts for pagination")
            total_items, total_pages = self._count_total(partial, pagination)
            pagination_results = {
                "items": total_items,
                "pages": total_pages
            }
            response["pagination"] = pagination_results

        return response

    def _apply_filters_clause(self, partial: Query, target: Table, filters: dict, operator: str) -> Query:
        """Apply filters with the right operator to the partial query.

        Filters are created with ``_prepare_filter_criteria``. Supercharge this
        method to customize filters.
        """
        operator = and_ if operator == PostInputFields.Operators.and_ else or_
        filter_criteria = self._prepare_filter_criteria(target, filters)

        if filter_criteria:
            partial = partial.filter(operator(*filter_criteria))
        return partial

    def _apply_order_by_clause(self, partial, order_by: List[Union[str, dict, list, tuple]]) -> Query:
        """Apply ``order_by`` clause to partial query getting given fields from the target table's model.

        Exceptions from preparing the clauses are caught individually so that all
        acceptable specifications will be added nonetheless. If the specification list
        is empty (or no specification is valid) nothing is done.
        """
        order_clauses = []
        for field in order_by:
            try:
                order_clauses.append(self.__prepare_order_by_element(self.target, field))
            except (TypeError, AttributeError, KeyError) as e:
                self.logger.error("Unable to add ordering clause for field %s : %s", field, repr(e))
                continue

        if order_clauses:
            partial = partial.order_by(*order_clauses)
        return partial

    @staticmethod
    def _get_page(partial: Query, pagination: dict) -> List[Table]:
        """Get results from partial query.

        Combine ``size`` and ``page`` to add limit and offset parameters to the
        partial query. ``pagination`` is a dictionary of the form ::

            {
                "size": 10,  # results by page, default to 10
                "page": 1    # page to request, defaulut to 1
            }
        """
        size = pagination.get(PostInputFields.Pagination.size, DEFAULT_PAGE_SIZE)
        page = pagination.get(PostInputFields.Pagination.page, DEFAULT_PAGE)
        offset = (page - 1) * size
        partial = partial.limit(size).offset(offset)
        return partial.all()

    @staticmethod
    def _count_total(partial: Query, pagination: dict) -> Tuple[int]:
        """Count total number of items matching the query.

        Return the total number of items, and the corresponding number of pages
        given the page size referred in ``pagination``.
        """
        size = pagination.get(PostInputFields.Pagination.size, DEFAULT_PAGE_SIZE)
        total_items = partial.order_by(None).count()
        total_pages = int(ceil(total_items / float(size)))
        return total_items, total_pages

    @staticmethod
    def __prepare_order_by_element(target: Table, field: Union[str, dict]):
        """Prepare an order_by column.

        Authorized field specifications are only a dictionary
        with ``field`` and optional ``direction`` keys (defaulted to ``asc``)::

            {
                "field": "column_name",
                "direction": "asc"
            }

        Possible raised errors are :

        * ``AttributeError`` if the target field is not found in the table
        * ``KeyError`` if the dict specification misses 'field' key
        * ``TypeError`` if the specification is not among the accepted types
        """
        if isinstance(field, dict):
            direction = field.get("direction", "asc").lower()
            column = getattr(target, field["field"])
            result = desc(column) if direction == "desc" else column
        else:
            msg = f"Not supported {type(field)} type for ordering field {field}"
            raise TypeError(msg)
        return result
