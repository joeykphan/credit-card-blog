""""Definition for Flask application and database instance."""
from typing import Any

from app import app, db
from app.models import Post, User


@app.shell_context_processor
def make_shell_context() -> dict[str, Any | None]:
    """Generate shell context for `flask shell`.

    Returns:
    -------
        dict: Object instances to inject into shell session.
    """
    return {"db": db, "User": User, "Post": Post}
