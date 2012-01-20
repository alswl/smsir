#!/usr/bin/env python
# coding=utf8

from datetime import datetime

from sqlalchemy import Column, Integer, String, Unicode, TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from config import Base, Session

class Phone(Base):
    """contact model"""
    __tablename__ = 'phone'

    id = Column(Integer, primary_key=True)
    number = Column(String(20), nullable=False)
    contact_id = Column(Integer, ForeignKey('contact.id'))
    #contact = relationship('Contact',
                           #primaryjoin='Contact.id == Phone.contact_id')
    create_at = Column(TIMESTAMP)

    def __init__(self, number=None):
        self.number = number
        self.create_at = datetime.now()

number_rule = r'\+?\d{11, 13}'
