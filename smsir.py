#!/usr/bin/env python
# coding=utf8
import argparse
import logging

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
import yaml

from config import Base, session, engine
from model.sms import Sms
from model.contact import Contact
from parser.best_message_storer_parser import Best_message_storer_parser

logger = logging.getLogger(__name__)

class Smsir(object):
    """A sms helper"""

    def __init__(self):
        self.Base = Base
        self.session = session
        self.engine = engine

    def run(self):
        parser = argparse.ArgumentParser(
            description='a sms console helper to manage sms'
            )
        parser.add_argument('--create', '-c',
                            action='store_true',
                            help='create a new database')
        parser.add_argument('--list-messages', '-l',
                            action='store_true',
                            help='list all messages')
        parser.add_argument('--import-sms-backup-restore', '-b',
                            type=argparse.FileType('r'),
                            metavar='FILE',
                            help='import messages from SMS Backup & Restore')
        parser.add_argument('--import-best-message-storer', '-B',
                            type=argparse.FileType('r'),
                            metavar='FILE',
                            nargs='+',
                            help='import messages from Best MessageStorer backups')
        args = parser.parse_args()

        if args.create:
            self.create_all()
        elif args.list_messages:
            self.list_messages()
        elif args.import_sms_backup_restore != None:
            pass
        elif args.import_best_message_storer != None:
            for text in args.import_best_message_storer:
                best_message_storer_parser = Best_message_storer_parser(
                    text.read().decode('utf-16le')
                    )
                smses = best_message_storer_parser.parse()
                session.add_all(smses)
                session.commit()
                best_message_storer_parser.print_result()
        else:
            parser.print_help()

    def create_all(self):
        self.Base.metadata.drop_all(checkfirst=True, bind=session.bind)
        self.Base.metadata.create_all(self.engine)

    def list_messages(self):
        print 'messages'
        pass

    def import_sms_backup_restore(self, texts):
        pass

    def import_best_message_storer(self, texts):
        textparser.parse(texts)

    def test(self):
        pass

def main():
    smsir = Smsir()
    smsir.run()

if __name__ == '__main__':
    main()
