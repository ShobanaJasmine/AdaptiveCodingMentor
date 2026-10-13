
import uuid


def create_attempt_id() -> str:
    """Generate a unique ID for a new coding submission."""
    return f"attempt-{uuid.uuid4()}"
