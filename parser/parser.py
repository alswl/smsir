#!/usr/bin/env python
#coding=utf-8

# desc: Parser
# author: alswl
# date: 2011-01-07

from model.sms import Sms

class Parser(object):
    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.format_error_count = 0
        self.duplicate_error_count = 0

    def parse(self, text):
        pass

class FormatError(ValueError):
    """非法格式"""
    pass

class DuplicateError(ValueError):
    """重复内容"""
    pass
