# Updated database.py to add email constraints and improve schema

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

# Updated User schema with email constraints
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    # Added email validation
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Email must contain an '@' symbol"
        return email

    # Additional relationships or methods can be added here

# Any other schemas should be updated here accordingly.