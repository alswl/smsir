#!/usr/bin/env python
#coding=utf-8

# desc: 更新短信联系人为空的短信
# author: alswl
# date: 2011-01-22

from sqlalchemy import and_

from model.sms import Sms
from config import Base, session, engine

def update_sms():
    """更新短信联系人为空的短信"""
    number_rows = session.execute("""
select distinct number, phone_id, contact_id
from sms
where contact_id is null;""")
    for row in number_rows.fetchall():
        number = row['number']
        sms = session.query(Sms).filter(
            and_(Sms.number.like('%' + number), Sms.contact_id != None)
            ).first()
        if sms is not None:
            session.execute(
                """
update sms
set contact_id = :contact_id, phone_id = :phone_id
where number =:number;""",
                {'contact_id': sms.contact_id,
                 'phone_id': sms.phone_id,
                 'number': sms.number}
                )
    session.commit()
