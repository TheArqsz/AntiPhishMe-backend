import json
import datetime

from db_config import db


class Certs(db.Model):
    __tablename__ = 'certs'
    id = db.Column(db.Integer(), primary_key=True)
    caid = db.Column(db.Integer(), unique=True, nullable=False)
    is_bad = db.Column(db.Boolean(), default=False)
    subject_organizationName = db.Column(db.String(160), nullable=False)
    subject_countryName = db.Column(db.String(160), nullable=False)
    issuer_commonName = db.Column(db.String(160), nullable=False)
    registered_at = db.Column(db.DateTime(), nullable=False)
    multi_dns = db.Column(db.Integer(), nullable=False)


    def json(self):
        return {
            'caid': self.caid, 
            'subject_organizationName': self.subject_organizationName,
            'subject_countryName': self.subject_countryName,
            'issuer_commonName': self.issuer_commonName,
            'registered_at': self.registered_at,
            'multi_dns': self.multi_dns,
            'is_bad': self.is_bad
            }

    @staticmethod
    def add_cert(
        _caid, 
        _subject_organizationName, 
        _subject_countryName, 
        _issuer_commonName, 
        _registered_at,
        _multi_dns,
        _is_bad=False
        ):
        new_cert = Certs(caid=_caid, 
        subject_organizationName=_subject_organizationName, 
        subject_countryName=_subject_countryName,
        issuer_commonName=_issuer_commonName,
        registered_at=_registered_at,
        multi_dns=_multi_dns,
        is_bad=_is_bad
        )
        db.session.add(new_cert)
        db.session.commit()

    @staticmethod
    def add_cert_td():
        Certs.add_cert(1, "Wojtek", "PL", "Arek", datetime.datetime.utcnow(), 1)
        Certs.add_cert(1644,  "Let's Encrypt", "EN", "Ola", datetime.datetime.utcnow(), 3, _is_bad=True)

    @staticmethod
    def get_all_certs():
        return [Certs.json(b) for b in Certs.query.all()]