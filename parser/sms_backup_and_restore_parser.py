#!/usr/bin/env python
#coding=utf-8

# desc: Parser for sms backup & restore on Android
# author: alswl
# date: 2011-01-21

import logging
import re
from datetime import datetime

from BeautifulSoup import BeautifulSoup

from model.sms import Sms
from model.contact import Contact
from model.phone import Phone
from parser import Parser, FormatError, DuplicateError
from config import Base, session

logger = logging.getLogger(__name__)

class SmsBackupAndRestoreParser(Parser):

    def __init__(self, xml):
        super(SmsBackupAndRestoreParser, self).__init__()
        self.xml = xml
        self.smses = []

    def parse(self):
        soup = BeautifulSoup(self.xml)
        for sms_node in soup.findAll('sms'):
            try:
                self.process_block(sms_node)
                self.success_count += 1
            except FormatError, e:
                #logger.info('%s is not illegal format' %block) # FIXME
                self.format_error_count += 1
                self.fail_count +=1
                continue
            except DuplicateError, e:
                self.duplicate_error_count +=1
                self.fail_count +=1
                continue
        return self.smses

    def print_result(self):
        print '# Success:\t%d' %self.success_count
        print '# Failed:\t%d' %self.fail_count
        print '# duplicate error\t%d' %self.duplicate_error_count
        print '# format error\t%d' %self.format_error_count

    def process_block(self, node):
        type_text = node.get('type')
        number = node.get('address')
        content = node.get('body')
        create_at = node.get('date')
        name = node.get('contact_name')

        if name == '(Unknown)':
            name = None
        if not type_text.isdigit() or \
           not create_at.isdigit():
            raise FormatError
        type = int(type_text)
        if number.find('+86') < 0: # fix number don't has +86
            number = '+86' + number
        create_at = datetime.fromtimestamp(float(create_at) / 1000)

        super(SmsBackupAndRestoreParser, self).save_sms(type,
                                                        name,
                                                        number,
                                                        content,
                                                        create_at)
