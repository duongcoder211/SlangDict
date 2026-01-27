from typing import Optional
from sqlmodel import SQLModel, Field

"""
The OperationalError: no such table: slang occurs because your model uses SQLAlchemy's Base while your table creation logic calls SQLModel.metadata.create_all.
In SQLAlchemy, a table is only created if it is registered in the specific MetaData object being used for the create_all call. 
"""
# USING SQLAlchemy
# from sqlalchemy import String, Text, Integer
# from sqlalchemy.orm import DeclarativeBase
# from sqlalchemy.orm import Mapped
# from sqlalchemy.orm import mapped_column
# from sqlalchemy.orm import relationship
# class Base(DeclarativeBase):
#     pass
# class Slang(Base):
#     __tablename__ = "slang"
#     id: Mapped[int] = mapped_column("Index", Integer, primary_key=True, autoincrement=True, nullable=False)
#     slang: Mapped[str] = mapped_column("Slang", Text, nullable=False)
#     mean: Mapped[Optional[str]] = mapped_column("Mean", Text, nullable=False)

#     def __repr__(self) -> str:
#         return f"Slang(id={self.id!r}, slang={self.slang!r}, mean={self.mean!r})"

# USING SQLModel
class Slang(SQLModel, table=True):
    __tablename__ = "slang"
    id: int | None = Field(description="Index", primary_key=True, unique=True, nullable=False)
    slang: str = Field(description="Slang", nullable=False, unique=True)
    mean: Optional[str] = Field(description="Mean", nullable=False)

    def __repr__(self) -> str:
        return f"Slang(id={self.id!r}, slang={self.slang!r}, mean={self.mean!r})"