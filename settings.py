import os
import dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


dotenv.load_dotenv()


class DatabaseConfig:
    DATABASE_NAME = os.getenv("DATABASE_NAME", "cats")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "2011")

    ROOT_DB_PASSWORD = os.getenv("DB_PASSWORD")
    ROOT_DB_USER = os.getenv("DB_USER", "postgres")

    SECRET_KEY = os.getenv("SECRET_KEY", "SECRET_KEY")

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
    MAX_FORM_MEMORY_SIZE = 1024 * 1024  # 1MB
    MAX_FORM_PARTS = 500

    NAME_RESTAURNAT = "Смачно Онлайн"

    def uri_postgres(self):
        return f"postgresql+psycopg2://{
            self.DB_USER}:{
            self.DB_PASSWORD}@localhost:5432/{
            self.DATABASE_NAME}"

    def uri_sqlite(self):
        return f"sqlite:///{self.DATABASE_NAME}.db"


config = DatabaseConfig()


engine = create_engine(config.uri_postgres(), echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    @classmethod
    def create_db(cls):
        cls.metadata.create_all(engine)

    @classmethod
    def drop_db(cls):
        cls.metadata.drop_all(engine)
