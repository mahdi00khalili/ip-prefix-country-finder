from sqlalchemy.orm import sessionmaker
from models.models import IpCountryLog
from sqlalchemy import inspect


# Define the listener functions

def log_ip_country_update(mapper, connection, target):
    """
    This function is triggered whenever there is an update on the Tag model.
    It logs the changes in the TagLog model.
    """
    session = sessionmaker(bind=connection)()

    # Inspect the target to access its state and track previous values
    state = inspect(target)

    for attr in state.attrs:
        if attr.history.has_changes():
            # Retrieve old and new values if there are changes
            old_value = attr.history.deleted[0] if attr.history.deleted else None
            new_value = getattr(target, attr.key)

            # Log the change in TagLog
            log_entry = IpCountryLog(
                ip_country_id=target.id,
                changed_column=attr.key,
                old_value=old_value,
                new_value=new_value,
                operation="UPDATE",
                changed_by="System",  # Replace with actual user context if available
            )
            session.add(log_entry)

    session.commit()


def log_ip_country_insertion(mapper, connection, target):
    """
    This function is triggered when a new Tag is inserted into the database.
    It logs the changes in the TagLog model for the initial values.
    """
    session = sessionmaker(bind=connection)()

    log_entry = IpCountryLog(
        ip_country_id=target.id,
        changed_column='multiple columns',
        old_value='',  # For new insertions, there is no old value
        new_value='',
        operation="INSERT",
        changed_by="System",  # Assuming system for now, this should ideally come from the tag context
    )
    session.add(log_entry)

    session.commit()
