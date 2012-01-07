#!/usr/bin/env python
#coding=utf-8

# desc: Parser
# author: alswl
# date: 2011-01-07

from sms import Sms

class TextParser(object):
    def __init__(self):
        pass

    def parse(self, text):
        sms = Sms()
        for block in text.split('================================' \
                                '======================================'):
            print line

        pass
