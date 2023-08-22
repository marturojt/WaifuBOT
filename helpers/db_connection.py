# mysql library
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from models.waifu_models import Base

# Database credentials
from data import db_options

# Database connection settings
connection_string = f"mysql+mysqlconnector://{db_options.user}:{db_options.password}@{db_options.host}/{db_options.database}"
engine = create_engine(connection_string)

# Create database if it does not exist.
if not database_exists(engine.url):
    create_database(engine.url)


# Create tables and session
Base.metadata.create_all(engine)
db_session = sessionmaker(bind=engine)
