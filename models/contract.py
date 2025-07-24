from sqlalchemy import Column, Integer, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship, validates

from .base import Base, TimestampMixin
from utils.validators import validate_positive_amount


class Contract(Base, TimestampMixin):
    """Contract model representing a contract in the system."""

    __tablename__ = "contracts"

    contract_id = Column(Integer, primary_key=True, autoincrement=True)
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    date_created = TimestampMixin.created_at
    is_signed = Column(Boolean, default=False, nullable=False)

    # Foreign keys
    client_id = Column(Integer, ForeignKey("clients.client_id"), nullable=False)
    sales_contact_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Relations
    client = relationship("Client", back_populates="contracts")
    sales_contact = relationship("User", back_populates="contracts")
    events = relationship("Event", back_populates="contract")

    # Validation methods
    @validates("total_amount", "remaining_amount")
    def validate_amounts(self, key, value):
        return validate_positive_amount(value, key)
    
    # Representation method
    def __repr__(self):
        status = "Signed" if self.is_signed is True else "Pending"
        return (f"<Contract {self.contract_id}: {status}>"
                f"Total: {self.total_amount}, Remaining: {self.remaining_amount}>")
