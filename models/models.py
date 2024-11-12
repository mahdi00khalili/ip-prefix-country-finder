from sqlalchemy import ForeignKey, String, Column, Integer, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class IpPerfix(Base):
    __tablename__ = 'ip_perfix'

    id = Column(Integer, primary_key=True)
    ip_perfix = Column(String(255))
    is_public = Column(Boolean, default=True)

    # Many-to-Many relationship with Country via IpCountry
    countries = relationship("Country", secondary="ip_countries", backref="ip_prefixes")


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
    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)
    ip_perfix_id = Column(Integer, ForeignKey('ip_perfix.id'), nullable=False)


class Log(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    changed_column = Column(String(50))
    old_value = Column(String)
    new_value = Column(String)
    operation = Column(String)
    changed_at = Column(DateTime(timezone=False), default=func.now())


class CountryLog(Log):
    __tablename__ = 'country_logs'

    country_id = Column(Integer, ForeignKey('countries.id'), nullable=False)  # ForeignKey added
    # No need for back_populates, backref is handling the reverse relationship


class IpCountryLog(Log):
    __tablename__ = 'ip_country_logs'

    ip_country_id = Column(Integer, ForeignKey('ip_countries.id'), nullable=False)  # ForeignKey added
    # No need for back_populates, backref is handling the reverse relationship
