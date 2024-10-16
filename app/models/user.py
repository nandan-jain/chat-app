import uuid

from app.core.database import Base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, text


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = Column(String, unique=True)
    phone_number = Column(String, nullable=True, unique=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, nullable=False)  # 'merchant' or 'customer'

    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    is_superuser = Column(Boolean, default=False)
    
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))