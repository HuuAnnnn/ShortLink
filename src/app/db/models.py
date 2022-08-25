from sqlalchemy import Column, String, Integer, Boolean
from .database import Base


class ShortLink(Base):
    __tablename__ = "ShortLink"
    short_url = Column(String, primary_key=True, index=True)
    long_url = Column(String, index=True)
    datetime = Column(String, index=True)
    access_count = Column(Integer, index=True)
    is_activate = Column(Boolean, index=True)
