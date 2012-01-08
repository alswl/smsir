#!/usr/bin/env python
#coding=utf-8

# desc: Parser
# author: alswl
# date: 2011-01-07

from model.sms import Sms

class Parser(object):
    def __init__(self):
        pass

    def parse(self, text):
        pass

class IllegalFormatError(ValueError):
    """非法格式"""
    pass

