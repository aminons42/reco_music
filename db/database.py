from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


DB_URL = mysql+pysql:root:admin123@loclhost:3306/reco_music
engine=create_engine(DB_URL)
Session=sessionmaker(bind=engine)
Base=declarative_base()

def get_db:
    db=Session()
    try:
        yield db:
    finally:
        db.close()
            