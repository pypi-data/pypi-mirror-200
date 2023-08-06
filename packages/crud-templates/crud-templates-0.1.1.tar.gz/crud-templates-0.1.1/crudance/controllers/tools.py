from datetime import datetime
from logging import getLogger
from typing import List

from sqlalchemy.orm import Session, Query
from sqlalchemy.schema import Table


class PostSearchTemplateTools:
    """Common internal methods for all controllers.

    This class is not meant to be used as such, it is a toolbox of building
    methods that will be used within methods of the child classes, mainly
    ``PostSearchControllerTemplate``.
    """
    JOINS_FILTERS = []          # see _prepare_joins_filters
    RANGE_FILTERS = []          # see _prepare_range_filters
    DATE_FIELDS = []            # see _serialize
    ENUM_FIELDS = []            # see _serialize
    LOOSE_STRING_FIELDS = []    # see _prepare_single_value_critteria

    def __init__(self, target: Table = None, session: Session = None) -> None:
        self.target = target
        self.session = session
        self.logger = getLogger(__name__)

    def _init_partial_query(self, filters: dict = None) -> Query:
        """Build SQLAlchemy partial query on target table and joins if needed.

        :param filters: Input filters for the search

        The method prepares a partial query on the target table. If no filters are
        provided, the query on the target table is returned as such. This is generally
        the desired behaviour for PUT, PATCH and DELETE controllers.

        If filters are provided, joins will be added to the query as specified
        within each element of ``JOINS_FILTER``.

        Each join filter in the input must provide a ``slot`` which is the name
        of the filtering dictionary within the input and a ``map_method``. The
        ``map_method`` is a handwritten method in the controller that append all
        needed joins for that filter to the partial query. The partial object
        and the corresponding filters from the input are passed as argument to
        the mapping method (in that order).
        """
        partial = self.session.query(self.target)
        if filters is None:
            return partial

        for join_filter in self.JOINS_FILTERS:
            if filters.get(join_filter["slot"]):
                self.logger.debug("Apply join for table %s from filter %s", join_filter["table"], join_filter["slot"])
                try:
                    map_method = getattr(self, join_filter.get("map_method"))
                except (AttributeError, TypeError):
                    # Attribute error if mispelled, TypeError if not defined (from None)
                    self.logger.debug(
                        "Unable to automatically join for filter %s, missing mapping method",
                        join_filter["slot"]
                    )
                    continue

                partial = map_method(partial, filters)
        return partial

    @classmethod
    def _serialize(cls, element: Table, selected_fields: list) -> dict:
        """Serialize an orm found element with given export fields.

        * a target field that is not found in the orm element is ignored and won't be returned
        * fields that appear in ``self.DATE_FIELDS`` will be serialized as isoformat date strings
        * fields that appear in ``self.ENUM_FIELDS`` will be serialized as strings
        """
        output = {}
        for export_field in selected_fields:
            try:
                output[export_field] = getattr(element, export_field)
            except AttributeError:
                continue
            if export_field in cls.DATE_FIELDS:
                output[export_field] = output[export_field].isoformat()
            if export_field in cls.ENUM_FIELDS:
                output[export_field] = output[export_field].value

        return output

    def _prepare_filter_criteria(self, target: Table, filters: dict) -> list:
        """Prepare sqlalchemy filter criteria to be added to a partial query.

        Return a list of sqlalchemy filtering criteria (such as comparisons,
        inclusions, etc.), that is ready to be wrapped within one or several
        `.filter()` parts of a query after joining with an ``and`` or ``or`` operator.

        :param target: Table to apply direct filters clause on (from the db model)
        :param filters: Filters to apply, can be column-value pairs, joined tables
            nested column-values pairs, or a range filter definition

        Usage
        =====

        Since it returns a list, it can be called several times provided you extend
        the previous resulting list with the result. In the ``PostSearchControllerTemplate``,
        it is called once by ``apply_filters_clause``, which joins all the element
        in the result with a logical operator then adds the ``.filter()`` to the
        partial query.

        It wraps building three types of filters that may cover most of the use-cases
        when searching within the database :

            * simple column-value filters on the main target table
            * simple column-value filters on joined tables (target may not be used)
            * specific range filters (numbers and dates) on any column of the join
              provided the join was actually added to the partial query
        """
        criteria = self.__prepare_single_value_criteria(target, filters)
        criteria.extend(self._prepare_joins_filters(filters))
        criteria.extend(self._prepare_range_filters(filters))
        return criteria

    def _prepare_joins_filters(self, filters: dict) -> List[str]:
        """Prepare single value filters on joined tables.

        This method wrap calls to ``__prepare_single_value_criteria`` by applying
        them to each of the joined table defined in ``self.JOINS_FILTER``, and is called
        during ``_prepare_filter_criteria``.

        Each element of attribute ``self.JOINS_FILTER`` must have two fields:

            * slot : the name of the filter in the input body (and schema)
            * table : the target joined table from the db model

        The method finds the filter definition from the slot name within the whole
        filters, and apply them to the target table. The partial query that the
        built filters will be added to **must contain the join with the target
        table already**.

        This is automatically handled by ``_init_partial_query`` and the ``map_method``
        referenced in the ``JOINS_FILTERS`` for straight cases.
        """
        criteria = list()
        for join_filter in self.JOINS_FILTERS:
            if filters.get(join_filter["slot"]):
                self.logger.debug("Apply join filter %s to table %s", join_filter["slot"], join_filter["table"])
                sub_filter_criteria = self.__prepare_single_value_criteria(
                    target=join_filter["table"],
                    filters=filters[join_filter["slot"]]
                )
                criteria.extend(sub_filter_criteria)
        return criteria

    def _prepare_range_filters(self, filters: dict) -> List[str]:
        """Prepare range filters.

        Much like ``_prepare_joins_filter``, it wraps calls to ``__prepare_range_criteria``
        to build range filters from the definitions found in ``self.RANGE_FITLERS``.
        It is called during ``_prepare_filter_criteria``.

        Each element of attribute ``self.RANGE_FILTERS`` has to mandatory fields
        and one optional :

            * slot : the name of the filter in the input body (and schema)
            * column : the column object model to apply the filter to
            * is_date : default ``False``, will build a date filter instead of a numbers filter

        If the range filter applies to columns from join tables, you have to
        supercharge or replace ``_init_partial_query`` to be sure that the join
        is actually added to the partial query when trying to filter with it,
        since there is no automatic join from range filters as we have for join filters.
        """
        criteria = list()
        for range_filter in self.RANGE_FILTERS:
            if filters.get(range_filter["slot"]):
                self.logger.debug("Apply range filter '%s' to column %s", range_filter["slot"], range_filter["column"])
                range_filter_criteria = self.__prepare_range_criteria(
                    filters=filters[range_filter["slot"]],
                    column=range_filter["column"],
                    is_date=range_filter.get("is_date", False)
                )
                criteria.extend(range_filter_criteria)
        return criteria

    def __prepare_single_value_criteria(self, target: Table, filters: dict) -> list:
        """Prepare simple column-value pairs filtering criteria.

        A filter is pair of a column name (from the db model) and a target value.
        For the usual value types the method automatically chooses the appropriate
        way of creating the filter clause.

        If the value of a pair is itself a dictionary, nothing is done for that pair
        since it is the signal for nested join or range filters.

        Recognized and handled value types are :

            * ilike comparison for strings
            * value comparison for enums
            * equality comparison for integers and floats
            * appartenance test for lists and tuples
            * equality for all other types

        For dates, it is preferable to use ``__prepare_range_filter``.
        """
        criteria = list()
        for field, value in filters.items():
            try:
                table_field = getattr(target, field)
            except AttributeError:
                self.logger.debug("Unable to find field %s in table %s", field, repr(target))
                continue

            if isinstance(value, str) and field in self.LOOSE_STRING_FIELDS:
                # Use ilike only if needed
                criteria.append(table_field.ilike(value))
            elif isinstance(value, list) or isinstance(value, tuple):
                # Use in operator for iterables
                criteria.append(table_field.in_(value))
            elif isinstance(value, dict):
                # Ignore nested filters
                continue
            else:
                # All other field types are defaulted to equality (int, float, str, enum, etc.)
                criteria.append(table_field == value)

        return criteria

    @staticmethod
    def __prepare_range_criteria(filters: dict, column, is_date: bool = False) -> list:
        """Create a filtering criteria for range filters.

        Create a range filter with lower, upper, or both bounds. Can be used
        for numbers and dates.

        :param filters: column-value pairs to filter on
        :param column: target column in table to filter on
        :param is_date: default False —— creates a date range filter instead of
           a numbers range, but note that the date has to be provided has a string
        """
        criteria = list()
        try:
            lower_bound = (
                datetime.fromisoformat(filters["lower_bound"])
                if is_date
                else filters["lower_bound"]
            )
        except KeyError:
            pass
        else:
            criteria.append(column >= lower_bound)

        try:
            upper_bound = (
                datetime.fromisoformat(filters["upper_bound"])
                if is_date
                else filters["upper_bound"]
            )
        except KeyError:
            pass
        else:
            criteria.append(column <= upper_bound)

        return criteria
