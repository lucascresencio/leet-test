from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.config.database import Base
from datetime import datetime


class WebhookLog(Base):
    __tablename__ = "webhook_logs"

    id = Column(Integer, primary_key=True, index=True)
    event = Column(String, nullable=False)
    payload = Column(JSON, nullable=False)
    received_at = Column(DateTime, default=datetime.utcnow)