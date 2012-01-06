# coding=utf8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

__all__ = ['Base', 'Session']

#engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///data.db', echo=True)

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())
Session.configure(bind=engine)
session =  Session()

# The declarative Base
Base = declarative_base()
