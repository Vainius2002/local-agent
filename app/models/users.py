from app.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    auth_user_id: Mapped[int] = mapped_column(Integer)
    username: Mapped[str] = mapped_column(String)
