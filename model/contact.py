#!/usr/bin/env python
# coding=utf8

from datetime import datetime

from sqlalchemy import Column, Integer, String, Unicode, TIMESTAMP
from sqlalchemy.orm import relationship, backref

from config import Base, session
from model.phone import Phone

class Contact(Base):
    """contact model"""
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)
    create_at = Column(TIMESTAMP)

    phones = relationship('Phone', backref='contact')

    def __init__(self, name=None):
        self.name = name
        self.create_at = datetime.now()

    def adjust_name(self):
        # TODO update for first name / last name
        self.name = self.name.replace(' ', '')
        self.name = self.name.replace('!', '')
        self.name = self.name.replace('！', '')
