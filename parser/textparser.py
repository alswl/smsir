#!/usr/bin/env python
#coding=utf-8

# desc: Parser
# author: alswl
# date: 2011-01-07

from model.sms import Sms

def parse(text):
    sms = Sms()
    for block in text.split('================================' \
                            '======================================'):
        print block

    pass
