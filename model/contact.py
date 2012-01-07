#!/usr/bin/env python
# coding=utf8

from sqlalchemy import Column, Integer, String, Unicode
from sqlalchemy.orm import relationship, backref

from meta import Base, session

class Contact(Base):
    """contact model"""
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)
    phone = Column(Integer(20), nullable=False)

    def __init__(self, name):
        self.name = name
