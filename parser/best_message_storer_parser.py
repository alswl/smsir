#!/usr/bin/env python
#coding=utf-8

# desc: Parser
# author: alswl
# date: 2011-01-07

import logging

from model.sms import Sms
from parser import Parser, IllegalFormatError

logger = logging.getLogger(__name__)

class Best_message_storer_parser(Parser):
    def __init__(self, text):
        self.text = text
        self.smses = []

    def parse(self):
        for block in self.text.split('======================================================================'):
            try:
                self.process_block(block)
            except IllegalFormatError, e:
                logger.info('%s is not illegal format' %block)
                continue
        return self.smses

    def process_block(self, text):
        sms = Sms()
        splits = text.split('----------------------------------------------------------------------')
        if len(splits) != 2:
            raise IllegalFormatError()
        meta = splits[0]
        content = splits[1].strip()
        logger.debug(content)
        # self.smses.append(sms)
