from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from ..db.connection import Base

class UpdateLog(Base):
    __tablename__ = 'update_logs'

    id = Column(Integer, primary_key=True, index=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    operation_type = Column(String(50), nullable=False)
    status = Column(String(20), nullable=False)
    error_message = Column(Text)
    retry_count = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    def __repr__(self):
        return f"<UpdateLog id={self.id} movie_id={self.movie_id} status={self.status}>"
