import datetime

from sqlalchemy import String, Integer, ForeignKey, Text, Date, Boolean, DateTime, ARRAY, func
from sqlalchemy.event import listens_for
from sqlalchemy.orm import mapped_column, Mapped, relationship, DeclarativeBase
from sqlalchemy_serializer import SerializerMixin

from typing import List


class Base(DeclarativeBase, SerializerMixin):
    pass


class User(Base):
    __tablename__ = "User"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    email: Mapped[str] = mapped_column(String(256), nullable=False)
    password: Mapped[str] = mapped_column(String(256), nullable=False)


class Task(Base):
    __tablename__ = "Task"
    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now())
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=datetime.datetime.now())
    datetime_to_do: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False)
    task_info: Mapped[str] = mapped_column(Text, nullable=False)
