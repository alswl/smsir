#!/usr/bin/env python
# coding=utf8

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from meta import Base, session

class Sms(Base):
    """sms model"""
    __tablename__ = 'sms'

    id = Column(Integer, primary_key=True)
    from_contact_id = Column(Integer, ForeignKey('contact.id'))
    from_contact = relationship('Contact', backref='sms')
                             
    content = Column(String(500))
    # TODO create_at

    def __init__(self):
        pass

    def add(self):
        session.add(self)
        session.commit()
