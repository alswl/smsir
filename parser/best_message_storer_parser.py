#!/usr/bin/env python
#coding=utf-8

# desc: Parser for Best message storer on Symbian
# author: alswl
# date: 2011-01-07

import logging
import re
import datetime

from model.sms import Sms
from model.contact import Contact
from model.phone import Phone
from parser import Parser, FormatError, DuplicateError
from config import Base, session

logger = logging.getLogger(__name__)

class Best_message_storer_parser(Parser):
    name_re = re.compile(
        ur'发件人: (\+?[\u2e80-\uffff|\s|\w|\d]+)\n' + '|' \
        ur'收件人: (\+?[\u2e80-\uffff|\s|\w|\d]+)\n'
        )
    number_re = re.compile(
        ur'发件人详情: (\+?[\u2e80-\uffff|\s|\w|\d]+)\n' + '|' + \
        ur'收件人详情: (\+?[\u2e80-\uffff|\s|\w|\d]+)\n'
        )
    type_re = re.compile(ur'文件夹: ([\u2e80-\uffff|\s]+)\n')
    create_at_re = re.compile(
        ur'日期/时间: (\d{4}年\d{1,2}月\d{1,2}日 /' \
        + ' \d{1,2}:\d{1,2}:\d{1,2} [ap]m)'
        )

    def __init__(self, text):
        super(Best_message_storer_parser, self).__init__()
        self.text = text
        self.smses = []

    def parse(self):
        for block in self.text.split('======================================================================'):
            try:
                self.process_block(block)
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

    def process_block(self, text):
        splits = text.split('----------------------------------------------------------------------')
        if len(splits) != 2:
            raise FormatError()
        meta = splits[0]
        content = splits[1].strip()
        if self.type_re.search(meta) is None or \
           self.name_re.search(meta) is None or \
           self.number_re.search(meta) is None or \
           self.create_at_re.search(meta) is None:
            raise FormatError()

        type = self.type_re.search(meta).group(1)
        name = self.name_re.search(meta).group(1) or \
                self.name_re.search(meta).group(2)

        if name is None:
            logger.error(meta)

        create_at_text = self.create_at_re.search(meta).group(1)
        create_at = datetime.datetime.strptime(
            create_at_text.replace(' am', '').replace(' pm', '').encode('utf-8'),
            u'%Y年%m月%d日 / %I:%M:%S'.encode('utf-8')
            )
        if create_at_text.find('pm') > 0:
            create_at += datetime.timedelta(hours=12)
        if type == u'发出的信息':
            number = self.number_re.search(meta).group(1)
            type_number = 2
        elif type == u'收件箱':
            number = self.number_re.search(meta).group(1)
            type_number = 1
        else:
            raise FormatError()
        if number.find('+86') < 0: # fix number don't has +86
            number = '+86' + number

        super(Best_message_storer_parser, self).save_sms(type,
                                                        name,
                                                        number,
                                                        content,
                                                        create_at)
