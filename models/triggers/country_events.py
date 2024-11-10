from sqlalchemy.orm import sessionmaker
from models.models import CountryLog

# Define the listener functions

def log_country_insertion(mapper, connection, target):
    """
    This function is triggered when a new Tag is inserted into the database.
    It logs the changes in the TagLog model for the initial values.
    """
    session = sessionmaker(bind=connection)()

    log_entry = CountryLog(
        country_id=target.id,
        changed_column='multiple columns',
        old_value='',  # For new insertions, there is no old value
        new_value='',
        operation="INSERT",
        changed_by="System",  # Assuming system for now, this should ideally come from the tag context
    )
    session.add(log_entry)

    session.commit()
