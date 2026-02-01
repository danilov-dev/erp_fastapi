from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[String] = mapped_column(String(50), unique=True, index=True, nullable=False)
    email: Mapped[String] = mapped_column(String(150), unique=True, index=True, nullable=False)
    password: Mapped[String] = mapped_column(String(150), nullable=False)  # TODO Написать метод хеширования пароля
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
