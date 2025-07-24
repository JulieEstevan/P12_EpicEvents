from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime, timezone

Base = declarative_base()


class TimestampMixin:
    """Mixin pour ajouter les timestamps created_at et updated_at"""

    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(
        DateTime, default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc), nullable=False
    )
