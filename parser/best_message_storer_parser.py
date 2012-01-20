#!/usr/bin/env python
#coding=utf-8

# desc: Parser
# author: alswl
# date: 2011-01-07

import logging
import re
import datetime

from model.sms import Sms
from model.contact import Contact
from model.phone import Phone
from parser import Parser, FormatError
from config import Base, session

logger = logging.getLogger(__name__)

class Best_message_storer_parser(Parser):
    name_re = re.compile(
        ur'发件人: (\+?[\u2e80-\uffff|\s|\w|\d]+)\n' + '|' \
        ur'收件人: (\+?[\u2e80-\uffff|\s|\w|\d]+)\n'
        )
    phone_re = re.compile(
        ur'发件人详情: (\+?[\u2e80-\uffff|\s|\w|\d]+)\n' + '|' + \
        ur'收件人详情: (\+?[\u2e80-\uffff|\s|\w|\d]+)\n'
        )
    type_re = re.compile(ur'文件夹: ([\u2e80-\uffff|\s]+)\n')
    create_at_re = re.compile(
        ur'日期/时间: (\d{4}年\d{1,2}月\d{1,2}日 /' \
        + ' \d{1,2}:\d{1,2}:\d{1,2} [ap]m)'
        )

    def __init__(self, text):
        self.text = text
        self.smses = []

    def parse(self):
        for block in self.text.split('======================================================================'):
            try:
                self.process_block(block)
            except FormatError, e:
                #logger.info('%s is not illegal format' %block) # FIXME
                continue
        return self.smses

    def process_block(self, text):
        splits = text.split('----------------------------------------------------------------------')
        if len(splits) != 2:
            raise FormatError()
        meta = splits[0]
        content = splits[1].strip()
        type = self.type_re.search(meta).group(1)
        name = self.name_re.search(meta).group(1) or \
                self.name_re.search(meta).group(2)

        if name is None:
            logger.error(meta)

        create_at = self.create_at_re.search(meta).group(1)
        if type == u'发出的信息':
            number = self.phone_re.search(meta).group(1)
            type_number = 2
        elif type == u'收件箱':
            number = self.phone_re.search(meta).group(1)
            type_number = 1
        else:
            raise FormatError()
        if number.find('+86') < 0: # fix number don't has +86
            number = '+86' + number

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

        sms = Sms()
        sms.create_at = datetime.datetime.strptime(
            create_at.replace(' am', '').replace(' pm', '').encode('utf-8'),
            u'%Y年%m月%d日 / %I:%M:%S'.encode('utf-8')
            )
        if create_at.find('pm') > 0:
            sms.create_at += datetime.timedelta(hours=12)
        sms.number = number
        sms.phone = phone
        sms.content = content
        sms.type = type_number
        #sms.update_contact()
        self.smses.append(sms)
