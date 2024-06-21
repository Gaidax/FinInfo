from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from app.database import Base


class SessionModel(Base):
    __tablename__ = "sessions"
    session_id = Column(String, nullable=False, unique=True)

    states = relationship("SessionStateModel", back_populates="session")
    data = relationship("SessionDataModel", back_populates="session")


class SessionStateModel(Base):
    __tablename__ = "session_states"
    parent_id = Column(Integer, ForeignKey("sessions.id"))
    state = Column(String, nullable=False)  # e.g., pan, eaadhaar
    status = Column(String, nullable=False)

    session = relationship("SessionModel", back_populates="states")

    __table_args__ = (UniqueConstraint("parent_id", "state"),)


class SessionDataModel(Base):
    __tablename__ = "session_data"
    parent_id = Column(Integer, ForeignKey("sessions.id"))
    tag = Column(String, nullable=False)
    data = Column(JSON, nullable=False)

    session = relationship("SessionModel", back_populates="data")
