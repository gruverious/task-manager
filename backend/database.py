from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

db_url=os.getenv("DATABASE_URL")
db_engine=create_engine(db_url)
db_session=sessionmaker(autocommit=False,autoflush=False,bind=db_engine)

ModelBase=declarative_base()

def get_database():
    database=db_session()
    try:
        yield database
    finally:
        database.close()