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
    content = Column(String(500))
    type = Column(Integer, nullable=False) # sms type: 1=inbox, 2=sendbox
    create_at = Column(TIMESTAMP)
    number = Column(String(20), nullable=False)
    phone_id = Column(Integer, ForeignKey('phone.id'))
    phone = relationship(
        'Phone',
        primaryjoin='Phone.id == Sms.phone_id',
        )
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

    def __init__(self, from_contact=None, to_contact=None):
        self.from_contact = from_contact
        self.to_contact = to_contact

    def update_contact(self, name):
        """update the number / contact info of sms"""
        contact = Session.query(Contact).filter_by(name=name).first()
        if contact == None:
            contact = Contact(name)
        phone = Session.query(Phone).filter_by(number=self.number).first()
