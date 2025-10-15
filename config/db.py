from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("mysql+pymysql://root:12345679@localhost:3306/test3")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

meta_data  = MetaData()

Base = declarative_base()


