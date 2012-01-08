#!/usr/bin/env python
# coding=utf8

from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

from config import Base, session

class Sms(Base):
    """sms model"""
    __tablename__ = 'sms'

    id = Column(Integer, primary_key=True)
    from_contact_id = Column(Integer, ForeignKey('contact.id'))
    to_contact_id = Column(Integer, ForeignKey('contact.id'))
    from_contact = relationship(
        'Contact',
        primaryjoin='Contact.id == Sms.from_contact_id',
        )
    to_contact = relationship(
        'Contact',
        primaryjoin='Contact.id == Sms.to_contact_id',
        )
                             
    content = Column(String(500))
    create_at = Column(TIMESTAMP)

    def __init__(self, from_contact=None, to_contact=None):
        self.from_contact = from_contact
        self.to_contact = to_contact

    def add(self):
        session.add(self)
        session.commit()
