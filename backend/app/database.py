from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:0123456789@db:3306/dictionary"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
