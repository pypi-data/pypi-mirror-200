from marshmallow import Schema, fields as mshm_fields
from marshmallow.validate import OneOf, Length, Range

from ..config import DEFAULT_PAGE_SIZE, DEFAULT_PAGE


AUTHORIZED_OPERATORS = ("and", "or")


class PostInputSchema(Schema):
    """Generic input schema for POST endpoints.

    All fields can be rewritten in the inherited schema, filters in particular that
    should be rewritten with a nested schema. ``fields`` and ``order_by`` can be
    limited to certain values using a validation with ``OneOf``.
    """
    class RangeFilterSchema(Schema):
        """Schema for range (number or date) filters.

        Note that dates will be converted by the filtering method, so string types
        work for both dates and numbers here.
        """
        lower_bound = mshm_fields.String(required=False)
        upper_bound = mshm_fields.String(required=False)

    class OrderBySpecificationSchema(Schema):
        """Schema for order by fields."""
        field = mshm_fields.String(required=True)
        direction = mshm_fields.String(required=False, load_default="asc", validate=OneOf(("desc", "asc")))

    class PaginationSchema(Schema):
        """Schema for pagination."""
        size = mshm_fields.Integer(required=False, load_default=DEFAULT_PAGE_SIZE)
        page = mshm_fields.Integer(required=False, load_default=DEFAULT_PAGE, validate=Range(min=1))
        compute = mshm_fields.Bool(required=False, load_default=False)

    filters = mshm_fields.Dict(required=True)  # Rewrite this field with the nested schema of desired Filters
    fields = mshm_fields.List(mshm_fields.String, validate=Length(min=1), required=True)
    order_by = mshm_fields.List(mshm_fields.Nested(OrderBySpecificationSchema), required=False)
    pagination = mshm_fields.Nested(PaginationSchema, required=False)
    operator_choice = mshm_fields.String(validate=OneOf(AUTHORIZED_OPERATORS), required=False)


class PostOutputSchema(Schema):
    """Generic output schema for POST endpoints.

    ``pagination`` field can be left as such, ``data`` must be rewritten in the
    inherited schema with the schema of output entities.
    """
    class Pagination(Schema):
        """Pagination schema."""
        items = mshm_fields.Integer(required=True)
        pages = mshm_fields.Integer(required=True)

    data = mshm_fields.List(mshm_fields.Dict(), required=True)  # Rewrite data field with the entities schema
    pagination = mshm_fields.Nested(Pagination, required=False)
