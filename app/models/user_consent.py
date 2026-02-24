from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.db import Base

class UserConsent(Base):
    __tablename__ = "user_consent"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    consent_type = Column(String, nullable=False)
    version = Column(String, nullable=False)
    accepted = Column(Boolean, default=True)
    scroll_completed = Column(Boolean, default=False)
    device_info = Column(String)
    ip_address = Column(String)
    accepted_at = Column(DateTime)
    revoked_at = Column(DateTime, nullable=True)
