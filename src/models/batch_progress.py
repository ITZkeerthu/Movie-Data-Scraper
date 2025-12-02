from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.sql import func
from ..db.connection import Base

class BatchProgress(Base):
    __tablename__ = 'batch_progress'

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(String(36), nullable=False)
    start_time = Column(TIMESTAMP, server_default=func.current_timestamp())
    end_time = Column(TIMESTAMP, nullable=True)
    total_records = Column(Integer, nullable=False)
    processed_records = Column(Integer, default=0)
    status = Column(String(20), nullable=False)
    last_processed_id = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<BatchProgress id={self.id} batch_id={self.batch_id} status={self.status}>"
