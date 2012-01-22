#!/usr/bin/env python
#coding=utf-8

# desc: Parser
# author: alswl
# date: 2011-01-07

from model.sms import Sms
from model.contact import Contact
from model.phone import Phone
from config import Base, session

class Parser(object):
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.format_error_count = 0
        self.duplicate_error_count = 0

    def parse(self, text):
        pass

    def save_sms(self, type, name, number, content, create_at):
        contact_phone_items = session.query(Contact, Phone). \
                filter(Contact.id == Phone.contact_id). \
                filter(Phone.number == number).all()
        if len(contact_phone_items) > 0:
            contact, phone = contact_phone_items[0]
        else:
            contact = Contact(name=name)
            phone = Phone(number)
            phone.contact = contact
            contact.adjust_name()
            session.add(contact)
            session.commit()

        sms = session.query(Sms).filter_by(number=number,
                                           create_at=create_at).first()
        if not sms is None: # 重复的短信
            raise DuplicateError

        sms = Sms()
        sms.create_at = create_at
        sms.number = number
        sms.phone = phone
        sms.content = content
        sms.type = type
        sms.contact = contact
        self.smses.append(sms)

class FormatError(ValueError):
    """非法格式"""
    pass

class DuplicateError(ValueError):
    """重复内容"""
    pass
