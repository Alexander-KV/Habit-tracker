from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(String(1000), default=None)
    completed: Mapped[bool] = mapped_column(default=False)