from marshmallow import Schema, INCLUDE


class AnySchema(Schema):
    """Any schema to allow unknown properties."""
    class Meta:
        """Unkown properties."""
        unknown = INCLUDE
