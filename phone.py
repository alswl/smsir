#!/usr/bin/env python
# coding=utf8

from sqlalchemy import Column, Integer, String, Unicode

from meta import Base, Session

class Phone(Base):
    """contact model"""
    __tablename__ = 'phone'

    id = Column(Integer, primary_key=True)
    number = Column(String(50), nullable=False)

