from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, Integer, Uuid
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from ppm_api.config import Settings


class Base(DeclarativeBase):
    pass


class FoundationState(Base):
    """Non-tenant installation metadata; no user or domain data."""

    __tablename__ = "foundation_state"
    __table_args__ = (CheckConstraint("id = 1", name="ck_foundation_singleton"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    instance_id: Mapped[UUID] = mapped_column(Uuid, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


def make_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(
        settings.database_url.get_secret_value(),
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=5,
        connect_args={"timeout": settings.dependency_timeout_seconds},
    )
