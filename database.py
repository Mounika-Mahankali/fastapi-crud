from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url="postgresql://postgres:mounika05@localhost:5432/fastapi_db"
engine=create_engine(db_url)
session=sessionmaker(autoflush=False,autocommit=False,bind=engine)