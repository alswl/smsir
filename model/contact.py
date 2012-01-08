#!/usr/bin/env python
# coding=utf8

from sqlalchemy import Column, Integer, String, Unicode, TIMESTAMP
from sqlalchemy.orm import relationship, backref

from config import Base, session

class Contact(Base):
    """contact model"""
    __tablename__ = 'contact'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)
    phone = Column(String(20), nullable=False)
    create_at = Column(TIMESTAMP)

    def __init__(self, name=None, phone=None):
        self.name = name
        self.phone = phone
