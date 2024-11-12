from sqlalchemy.orm import sessionmaker
from models.models import IpCountryLog
from sqlalchemy import inspect


# # Define the listener functions
#
# def log_ip_country_update(mapper, connection, target):
#     """
#     This function is triggered whenever there is an update on the Tag model.
#     It logs the changes in the TagLog model.
#     """
#     session = sessionmaker(bind=connection)()
#
#     # Inspect the target to access its state and track previous values
#     state = inspect(target)
#
#     for attr in state.attrs:
#         if attr.history.has_changes():
#             # Retrieve old and new values if there are changes
#             old_value = attr.history.deleted[0] if attr.history.deleted else None
#             new_value = getattr(target, attr.key)
#
#             # Log the change in TagLog
#             log_entry = IpCountryLog(
#                 ip_country_id=target.id,
#                 changed_column=attr.key,
#                 old_value=old_value,
#                 new_value=new_value,
#                 operation="UPDATE",
#             )
#             session.add(log_entry)
#
#     session.commit()


def log_ip_country_insertion(mapper, connection, target):

    session = sessionmaker(bind=connection)()

    log_entry = IpCountryLog(
        ip_country_id=target.id,
        changed_column='multiple columns',
        old_value='',  # For new insertions, there is no old value
        new_value='',
        operation="INSERT",
    )
    session.add(log_entry)

    session.commit()

def log_ip_country_deletion(mapper, connection, target):

    session = sessionmaker(bind=connection)()

    log_entry = IpCountryLog(
        ip_country_id=target.id,
        changed_column='',
        old_value='',  # For new insertions, there is no old value
        new_value='',
        operation="delete",
    )
    session.add(log_entry)

    session.commit()



