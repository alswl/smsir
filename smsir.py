#!/usr/bin/env python
# coding=utf8

from meta import session, Base
from sms import Sms
from contact import Contact

class Smsir(object):
    """A sms helper"""

    def __init__(self, session, Base):
        self.session = session
        self.Base = Base

    def create_all(self):
        Base.metadata.create_all()

    def import_from_xml(self):
        pass

    def import_from_txt(self):
        pass

    def test(self):
        sms = Sms()
        sms.from_contact = Contact(u'路飞')
        sms.add()
