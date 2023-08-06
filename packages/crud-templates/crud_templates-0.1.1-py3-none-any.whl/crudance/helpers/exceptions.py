class MissingIdentifyingField(ValueError):
    """Input body misses one or more identifying fields for entities."""
    pass


class EntityNotFound(ValueError):
    """Given entity was not found in database."""
    pass
