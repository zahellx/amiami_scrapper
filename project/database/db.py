from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('mysql+pymysql://user:password@amiami_mysql_amiami_1/db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()