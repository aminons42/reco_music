from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


DB_URL ="mysql+pymysql://root:admin123@localhost:3306/reco_music"
engine=create_engine(DB_URL)
Session=sessionmaker(bind=engine)
Base=declarative_base()

def get_db():
    db=Session()
    try:
        yield db
    finally:
        db.close()
            