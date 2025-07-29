from enum import Enum
from sqlalchemy import Column, Integer, String, Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship, validates
from argon2 import PasswordHasher
import argon2.exceptions

from .base import Base
from utils.validators import validate_email, validate_string_length, validate_phone_number


ph = PasswordHasher()


class UserRole(str, Enum):
    """Enum for user roles."""

    SALES = "SALES"
    SUPPORT = "SUPPORT"
    MANAGEMENT = "MANAGEMENT"

class User(Base):
    """User model representing a user in the system."""

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=True)
    hashed_password = Column(String(128), nullable=False)
    role = Column(SQLAlchemyEnum(UserRole), nullable=False)

    # Relations
    clients = relationship("Client", back_populates="sales_contact")
    contracts = relationship("Contract", back_populates="sales_contact")
    events = relationship("Event", back_populates="support_contact")

    # Password management methods
    def set_password(self, password: str):
        """Hash and set the user's password."""
        self.hashed_password = ph.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify the user's password."""
        if isinstance(self.hashed_password, Column):
            raise TypeError("hashed_password is not set")
        try:
            return ph.verify(self.hashed_password, password)
        except argon2.exceptions.VerifyMismatchError:
            return False
    
    # Validation methods
    @validates("email")
    def validate_email_address(self, key, address):
        return validate_email(address).strip().lower()

    @validates("first_name", "last_name")
    def validate_name_length(self, key, value):
        return validate_string_length(value, key, 50)

    @validates("phone_number")
    def validate_phone(self, key, number):
        return validate_phone_number(number)
    
    # Representation method
    def __repr__(self):
        return (
            f"<Employee {self.employee_id}: {self.first_name} "
            f"{self.last_name} ({self.department.value})>"
        )
