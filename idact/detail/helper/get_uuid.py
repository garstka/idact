import uuid


def get_uuid() -> str:
    """Returns a UUID as string."""
    return str(uuid.uuid1())
