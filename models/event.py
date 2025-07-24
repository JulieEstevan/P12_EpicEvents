from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, validates

from .base import Base, TimestampMixin
from utils.validators import validate_string_length, validate_positive_integer


class Event(Base, TimestampMixin):
    """Event model representing an event in the system."""

    __tablename__ = "events"

    event_id = Column(Integer, primary_key=True, autoincrement=True)
    event_name = Column(String(100), nullable=False)
    event_start_date = Column(DateTime, nullable=False)
    event_end_date = Column(DateTime, nullable=False)
    location = Column(String(200), nullable=False)
    attendees_count = Column(Integer, nullable=False)
    notes = Column(String(500), nullable=True)

    # Foreign keys
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.contract_id"), nullable=False)
    support_contact_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Relations
    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="events")
    support_contact = relationship("User", back_populates="events")

    # Validation methods
    @validates("name")
    def validate_name_length(self, key, value):
        return validate_string_length(value, key, 100)

    @validates("location")
    def validate_location_length(self, key, value):
        return validate_string_length(value, key, 200)

    @validates("description")
    def validate_description_length(self, key, value):
        return validate_string_length(value, key, 500)

    @validates("attendees_count")
    def validate_attendees_count(self, key, value):
        return validate_positive_integer(value, key)
    
    # Representation method
    def __repr__(self):
        return f"<Event {self.event_id}: {self.event_name} for {self.client.full_name}>"
