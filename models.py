from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import String, DateTime, ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from settings import Base, Session, engine
from sqlalchemy import select


class User(UserMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    orders = relationship(
        "Order",
        foreign_keys="Order.user_id",
        back_populates='user',
        cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"User({self.username})"

    @staticmethod
    def get(user_id: int):
        with Session() as session:
            return session.scalar(select(User).where(User.id == user_id))

    @staticmethod
    def get_by_username(username: str):
        with Session() as session:
            return session.scalar(select(User).where(User.username == username))


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(nullable=False)
    stock: Mapped[int] = mapped_column(default=0)
    image_url: Mapped[str] = mapped_column(String(255), nullable=True)


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    order_data: Mapped[dict] = mapped_column(JSONB)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")


def init_db():
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA public CASCADE"))
        conn.execute(text("CREATE SCHEMA public"))
        conn.commit()
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()