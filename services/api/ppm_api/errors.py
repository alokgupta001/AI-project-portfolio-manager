"""Only deliberate, credential-free business errors may reach a client."""

from fastapi import HTTPException


class DomainError(HTTPException):
    """Trusted public message; driver and unexpected exception text stays private."""
