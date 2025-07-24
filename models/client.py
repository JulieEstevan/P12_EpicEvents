from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, validates

from .base import Base, TimestampMixin
from utils.validators import validate_email, validate_string_length, validate_phone_number


class Client(Base, TimestampMixin):
    """Client model representing a client in the system."""

    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=True)
    company_name = Column(String(100), nullable=True)
    first_contact = TimestampMixin.created_at
    last_contact = TimestampMixin.updated_at

    # Foreign keys
    sales_contact_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Relations
    sales_contact = relationship("User", back_populates="clients")
    events = relationship("Event", back_populates="client")
    contracts = relationship("Contract", back_populates="client")

    # Validation methods
    @validates("name")
    def validate_full_name_length(self, key, value):
        return validate_string_length(value, key, 100)

    @validates("email")
    def validate_email_address(self, key, address):
        return validate_email(address).strip().lower()
    
    @validates("phone")
    def validate_phone_number(self, key, value):
        return validate_phone_number(value)
    
    @validates("company_name")
    def validate_company_name_length(self, key, value):
        return validate_string_length(value, key, 100)

    # Representation method
    def __repr__(self):
        return f"<Client {self.full_name} from {self.company_name}>"
    