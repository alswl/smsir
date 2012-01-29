#!/usr/bin/env python
#coding=utf-8

# desc: 合并联系人
# author: alswl
# date: 2011-01-29

from sqlalchemy import and_
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from model.sms import Sms
from model.contact import Contact
from config import Base, session, engine

def merge_contact(name_a, name_b):
    """合并联系人A->B"""
    try:
        contact_a, contact_b = get_contacts(name_a, name_b)
    except NoResultFound, e1:
        raise ValueError
    except MultipleResultsFound, e1:
        raise ValueError
    session.execute(
        """ update phone set contact_id=:id_b where contact_id=:id_a""",
        ({'id_a': contact_a.id, 'id_b': contact_b.id})
        )
    session.execute(
        """ update sms set contact_id=:id_b where contact_id=:id_a""",
        ({'id_a': contact_a.id, 'id_b': contact_b.id})
        )
    session.delete(contact_a)
    session.commit()

def get_contacts(name_a, name_b):
    contact_a = session.query(Contact).filter_by(name=name_a).one()
    contact_b = session.query(Contact).filter_by(name=name_b).one()
    return contact_a, contact_b
