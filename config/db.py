from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://root:12345679@localhost:3306/test")