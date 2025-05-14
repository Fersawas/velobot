from datetime import datetime
from enum import StrEnum

from sqlalchemy import Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    declared_attr,
    Mapped,
    mapped_column,
    relationship,
)
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.dialects.postgresql import ENUM, JSONB


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower() + "s"


class OrderStatus(StrEnum):
    NEW = "В очереди"
    IN_WORK = "В работе"
    READY = "Готов к выдаче"
    CLOSED = "Выполнен"
    CANCELLED = "Отменен"
    TROUBLES = "Не выполнен"

    @classmethod
    def list(cls):
        return [e.value for e in cls]


class Order(Base):
    # Order data
    title: Mapped[str] = mapped_column(String(400))
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    model_type: Mapped[str | None] = mapped_column(String(150), nullable=True)
    status: Mapped[OrderStatus] = mapped_column(
        ENUM(*OrderStatus.list(), name="order_status_enum", create_type=True),
        default=OrderStatus.NEW,
    )

    # Payment fields
    price_estimate: Mapped[float | None] = mapped_column(Float, nullable=True)
    final_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    is_paid: Mapped[bool] = mapped_column(default=False)
    expectation_date: Mapped[datetime | None] = mapped_column(  # Можно убрать
        DateTime, default=None, nullable=True
    )

    # Client info
    fullname: Mapped[str | None] = mapped_column(String(150), nullable=True)
    phone: Mapped[str] = mapped_column(String(20))

    # Additional info
    master_id: Mapped[int | None] = mapped_column(ForeignKey("admins.id"))
    master: Mapped["Admin"] = relationship("Admin", back_populates="master_orders")
    comment: Mapped[str | None] = mapped_column(String(200), nullable=True)
    photos: Mapped[list["Photo"]] = relationship("Photo", back_populates="order")


class Photo(Base):
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    photos_list: Mapped[list[str]] = mapped_column(JSONB)

    order: Mapped[Order] = relationship("Order", back_populates="photos")


class AdminRights(StrEnum):
    BASE = "Сотрудник"
    ADMIN = "Администратор"
    SUPERUSER = "Суперпользователь"

    @classmethod
    def list(cls):
        return [e.value for e in cls]


class Admin(Base):
    username: Mapped[str] = mapped_column(String(100), unique=True)
    phone: Mapped[str | None] = mapped_column(String(20))
    rights: Mapped[AdminRights] = mapped_column(
        ENUM(*AdminRights.list(), name="admin_rights_enum", create_type=True),
        default=AdminRights.BASE,
    )
    master_orders: Mapped[list["Order"]] = relationship(
        "Order", back_populates="master"
    )


class User(Base):
    username: Mapped[str | None] = mapped_column(String(100))
    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    phone: Mapped[str | None] = mapped_column(String(100))
    user_id: Mapped[int] = mapped_column(Integer)
