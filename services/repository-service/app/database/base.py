from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models so SQLAlchemy registers them
from app.models.repository import Repository
from app.models.source_file import SourceFile