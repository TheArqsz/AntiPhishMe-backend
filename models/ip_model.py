import json
import datetime

from db_config import db


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
        db.session.commit()

    @staticmethod
    def add_ip_td():
        IP.add_ip('127.0.0.1')

    @staticmethod
    def get_all_ip():
        return [IP.json(b) for b in IP.query.all()]