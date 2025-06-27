from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import String, DateTime, ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB
from settings import Base, Session
from werkzeug.security import generate_password_hash


class User(UserMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(
        String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False)

    orders = relationship(
        "Order",
        foreign_keys="Order.user_id",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"User({self.username})"

    @staticmethod
    def get(user_id: int):
        with Session() as conn:
            stmt = select(User).where(User.id == user_id)
            user = conn.scalar(stmt)
            if user:
                return user

    @staticmethod
    def get_by_username(username):
        with Session() as conn:
            stmt = select(User).filter_by(username=username)
            user = conn.scalar(stmt)
            return user if user else None


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
    order_time: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(String(30), default="pending")
    order_data: Mapped[dict] = mapped_column(JSONB)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user = relationship("User", back_populates="orders")


class Asortiment(Base):
    __tablename__ = "asortiment"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String, nullable=True)
    price: Mapped[float] = mapped_column()
    file_name: Mapped[str] = mapped_column(String)


def init_db():
    Base.drop_db()
    Base.create_db()

    user_admin = User(
        username="admin",
        email="ax@gmail.com",
        password=generate_password_hash("admin"),
        is_admin=True,
    )

    m1 = Asortiment(
        name="Хліб",
        description="Ароматний домашній хліб з натуральних інгредієнтів",
        price=25,
        file_name="https://bohlib.com.ua/wp-content/uploads/2024/08/pro-khlib-yakist-tradytsii-ta-maysternist-u-kozhnomu-shmatochku.jpg",
    )

    m2 = Asortiment(
        name="Ковбаса",
        description="Свіжа ковбаса з натуральних інгредієнтів, збережена за оптимальних умов",
        price=100,
        file_name="https://bmk.net.ua/wp-content/uploads/2023/03/%D0%9A%D0%BE%D0%B2%D0%B1%D0%B0%D1%81%D0%B0-%D1%81%D0%B0%D0%BB%D1%8F%D0%BC%D1%96-%D1%81%D0%B8%D1%80%D0%BE%D0%BA%D0%BE%D0%BF%D1%87%D0%B5%D0%BD%D0%B0-%D0%BF%D0%B5%D1%80%D1%88%D0%BE%D0%B3%D0%BE-%D1%81%D0%BE%D1%80%D1%82%D1%83-%D0%97%D0%BE%D0%BB%D0%BE%D1%82%D0%B0.jpg",
    )

    m3 = Asortiment(
        name="Огірки",
        description="Огірки мають свіжий зелений колір, соковиту м’якоть і хрустку текстуру",
        price=30,
        file_name="https://st3.depositphotos.com/1642482/19429/i/450/depositphotos_194294298-stock-photo-cucumber-and-slices.jpg",
    )

    m4 = Asortiment(
        name="Морква",
        description="Свіжа морква — тверда, соковита, яскраво-оранжева, без тріщин і темних плям.",
        price=20,
        file_name="https://www.bigom.lviv.ua/image/cache/catalog/PRODUCTS/morkva-shantane-23704334012166_small11-600x315.jpg",
    )

    m5 = Asortiment(
        name="Капуста",
        description="Капуста — щільний качан із хрустким листям і ніжним смаком.",
        price=40,
        file_name="https://img.freepik.com/premium-vector/white-cabbage-from-multicolored-paints-splash-watercolor-colored-drawing-realistic_537015-50.jpg",
    )

    m6 = Asortiment(
        name="Булка з маком",
        description="Булка з маком — м’яка, солодка, з ароматним маком зверху.",
        price=25,
        file_name="https://memepedia.ru/wp-content/uploads/2017/12/hqdefault.jpg",
    )

    m7 = Asortiment(
        name="Сир",
        description="Натуральний сир із ніжним смаком.",
        price=75,
        file_name="https://cdn.abo.media/upload/article/o_1f6hhm444a71hmqokq1k8b1sj035.jpg",
    )

    m8 = Asortiment(
        name="Помідор",
        description="Соковитий, стиглий помідор з насиченим смаком.",
        price=20,
        file_name="https://konkurent.ua/media/uploads/prev/2025/05/20/17/56/11/14556577856678678.png",
    )

    m9 = Asortiment(
        name="Вода",
        description="Звичайна вода.",
        price=20,
        file_name="https://aqualife.ru/upload/iblock/230/230712de973388a811758eb2e6c61926.jpg",
    )

    with Session() as conn:
        conn.add_all([user_admin, m1, m2, m3, m4, m5, m6, m7, m8, m9])
        conn.commit()


if __name__ == "__main__":
    init_db()
