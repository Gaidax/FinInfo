from datetime import datetime
from sqlalchemy import create_engine, func
from app.config import settings

from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column

SQLALCHEMY_DATABASE_URL = settings.database_url

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(nullable=True, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        nullable=True, default=func.now(), onupdate=func.now()
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
