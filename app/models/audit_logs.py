from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime
from datetime import datetime
from app.core.db import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True)
    action = Column(String, nullable=False)
    user_id = Column(Integer)
    details = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)