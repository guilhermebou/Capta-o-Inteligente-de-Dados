from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import getpass

user = input("USER: ")
password = getpass.getpass("PASSWORD: ")
database = "folks"
host = "localhost"

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}:5432/{database}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
