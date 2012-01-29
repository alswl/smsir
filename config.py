# coding=utf8

import logging
import logging.config
import yaml

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine

import sys
reload(sys)
sys.setdefaultencoding(sys.getfilesystemencoding()) # for cross-platform

config = yaml.load(open('config.yml', 'r'))

engine = create_engine(config['main']['data'], echo=True) # set data connect string

# SQLAlchemy session manager. Updated by model.init_model()
Session = scoped_session(sessionmaker())
Session.configure(bind=engine)
session =  Session()

# The declarative Base
Base = declarative_base()

logging.config.dictConfig(config['logging'])
