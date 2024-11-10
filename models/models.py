from sqlalchemy import ForeignKey, String, Column, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    abbr = Column(String(3), nullable=False)

    # Relationship with CountryLog using backref
    logs = relationship("CountryLog", backref="country")

class IpCountry(Base):
    __tablename__ = 'ip_countries'

    id = Column(Integer, primary_key=True)
    ip_prefix = Column(String(20), nullable=False)
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)

    country = relationship("Country")

    # Relationship with IpCountryLog using backref
    logs = relationship("IpCountryLog", backref="ip_country")


class Log(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    changed_column = Column(String(50))
    old_value = Column(String)
    new_value = Column(String)
    operation = Column(String)
    changed_by = Column(String)
    changed_at = Column(DateTime(timezone=False), default=func.now())


class CountryLog(Log):
    __tablename__ = 'country_logs'

    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)  # ForeignKey added
    # No need for back_populates, backref is handling the reverse relationship


class IpCountryLog(Log):
    __tablename__ = 'ip_country_logs'

    ip_country_id = Column(Integer, ForeignKey('ip_countries.id'), nullable=False)  # ForeignKey added
    # No need for back_populates, backref is handling the reverse relationship
