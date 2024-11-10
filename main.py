from models.models import Country, IpCountry
from sqlalchemy import create_engine, event
from models.base import Base
from sqlalchemy.orm import sessionmaker
from models.triggers.country_events import *
from models.triggers.ip_country_events import *

# Set up the engine for connecting to an SQLite database
DATABASE_PATH = "./ip_perfix_country_finder.sqlite"
engine = create_engine(f"sqlite:///{DATABASE_PATH}")

# Create a configured session class bound to the engine
Session = sessionmaker(bind=engine)  # This creates a factory for new Session objects
session = Session()  # Instantiate a new session for interacting with the database

# Create all tables defined in the Base's metadata; run this only once to set up the database schema
Base.metadata.create_all(engine)


def fire_events(model_name, model_str_name):
    # Attach event listeners to model

    event.listen(model_name, 'after_insert', globals()[f'log_{model_str_name}_insertion'])
    if model_name == 'ip_country':
        event.listen(model_name, 'after_update', globals()[f'log_{model_str_name}_update'])


fire_events(Country, 'country')
fire_events(IpCountry, 'ip_country')
