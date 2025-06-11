from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_URL ="mysql+pymysql://root:root@mysql:3306/musicdb"
engine=create_engine(DB_URL)
Session=sessionmaker(bind=engine)
Base=declarative_base()

def get_db():
    db=Session()
    try:
        yield db
    finally:
        db.close()
            