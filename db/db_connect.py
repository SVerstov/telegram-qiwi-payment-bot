from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import POSTGRES_ENGINE, DEBUG
from db.models import Base

if DEBUG:
    engine = create_engine('sqlite:///db/sqlite3.db')
else:
    engine = create_engine(POSTGRES_ENGINE)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

