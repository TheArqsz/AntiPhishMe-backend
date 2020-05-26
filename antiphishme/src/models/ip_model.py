import json
import datetime
import sqlalchemy

from antiphishme.src.db_config import db


class IP(db.Model):
    __tablename__ = 'ip'
    id = db.Column(db.Integer(), primary_key=True)
    ip = db.Column(db.String(60), unique=True, nullable=False)
    country = db.Column(db.String(10))
    asn = db.Column(db.String(60))


    def json(self):
        return {
            'ip': self.ip,
            'country': self.country,
            'asn': self.asn
            }

    @staticmethod
    def add_ip(
        _ip,
        _country=None,
        _asn=None
        ):
        new_ip = IP(ip=_ip, country=_country, asn=_asn)
        db.session.add(new_ip)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
        return IP.query.filter(IP.ip == _ip).first().id

        

    @staticmethod
    def add_ip_td():
        IP.add_ip('8.8.8.8', 'US', 'AS15169 Google LLC')
        IP.add_ip('4.4.4.4', 'US', 'AS3356 Level 3 Parent, LLC')
        IP.add_ip('1.1.1.1', 'AU', 'AS13335 Cloudflare, Inc.')
        IP.add_ip('156.17.93.11', 'PL', 'AS8970 Wroclaw Centre of Networking and Supercomputing')

    @staticmethod
    def get_all_ip():
        return [IP.json(b) for b in IP.query.all()]
