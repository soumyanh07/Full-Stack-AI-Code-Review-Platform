from sqlalchemy import Column, ForeignKey, Integer, String, Text, JSON
from sqlalchemy.orm import relationship

from app.database.base import Base


class SourceFile(Base):
    __tablename__ = "source_files"

    id = Column(Integer, primary_key=True, index=True)

    repository_id = Column(
        Integer,
        ForeignKey("repositories.id"),
    )

    path = Column(String(1000))
    language = Column(String(50))
    content = Column(Text)
    source_metadata = Column(JSON, nullable=True)

    repository = relationship(
        "Repository",
        back_populates="files",
    )