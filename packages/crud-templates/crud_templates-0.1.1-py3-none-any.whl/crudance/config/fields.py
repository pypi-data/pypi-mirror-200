class PostInputFields:
    """Generic fields for POST input or output."""
    class Pagination:
        """Fields for pagination."""
        size = "size"
        page = "page"
        total = "compute"

    fields = "fields"
    filters = "filters"
    order_by = "order_by"
    pagination = "pagination"
    operator_choice = "operator_choice"

    class Operators:
        """Authorized boolean operators for filters."""
        and_ = "and"
        or_ = "or"
