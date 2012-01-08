#!/usr/bin/env python
#coding=utf-8

# desc: Parser
# author: alswl
# date: 2011-01-07

import logging
import re

from model.sms import Sms
from parser import Parser, IllegalFormatError

logger = logging.getLogger(__name__)

class Best_message_storer_parser(Parser):
    name_re = re.compile(ur'[发件人|收件人]: (\+?[\u2e80-\uffff|\s|\w|\d]+)\n')
    type_re = re.compile(ur'文件夹: ([\u2e80-\uffff|\s]+)\n')

    def __init__(self, text):
        self.text = text
        self.smses = []

    def parse(self):
        for block in self.text.split('======================================================================'):
            try:
                self.process_block(block)
            except IllegalFormatError, e:
                #logger.info('%s is not illegal format' %block) # FIXME
                continue
        return self.smses

    def process_block(self, text):
        sms = Sms()
        splits = text.split('----------------------------------------------------------------------')
        if len(splits) != 2:
            raise IllegalFormatError()
        meta = splits[0]
        content = splits[1].strip()

        type = self.type_re.search(meta).group(1)
        name =  self.name_re.search(meta).group(1) # TODO
        logger.debug(name)
        if type == u'发出的信息':
            pass
        elif type == u'收件箱':
            pass
        else:
            raise IllegalFormatError()
        # self.smses.append(sms)
