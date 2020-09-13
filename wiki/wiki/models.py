from sqlalchemy import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, String, Date, DateTime, Float, Boolean, Text)
from scrapy.utils.project import get_project_settings

Base = declarative_base()


def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    Base.metadata.create_all(engine)


class Events(Base):
    __tablename__ = "events"

    day = Column('DAY', String)
    year = Column('YEAR', Integer)
    event = Column('EVENT', Text, primary_key=True)
    type_of_event = Column('TYPE_OF_EVENT', String)
    AD_BC = Column('AD/BC', String)
    date = Column('DATE', Date)
