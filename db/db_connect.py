from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import POSTGRES_ENGINE, DEBUG
from db.models import Base

engine = create_engine(POSTGRES_ENGINE, echo=DEBUG)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

