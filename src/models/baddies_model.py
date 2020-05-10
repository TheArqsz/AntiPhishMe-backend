import json
import datetime
import sqlalchemy

from db_config import db


class Baddies(db.Model):
    __tablename__ = 'baddies'
    id = db.Column(db.Integer(), primary_key=True)
    domain_name = db.Column(db.String(120), unique=True, nullable=False)
    ip_id = db.Column(db.Integer(), db.ForeignKey("ip.id"))
    crt_id = db.Column(db.Integer(), db.ForeignKey("certs.id"))
    levenstein_dist = db.Column(db.Integer())
    levenstein_matched_keyword = db.Column(db.String(60))
    contained_matched_keyword = db.Column(db.String(60))
    entropy = db.Column(db.Integer())
    timestamp_added = db.Column(db.DateTime(), default=datetime.datetime.utcnow)

    #TODO Edit fields (eg. crt_id)
    def json(self):
        return {
            'domain_name': self.domain_name, 
            'levenstein_dist': self.levenstein_dist,
            'entropy': self.entropy,
            }

    @staticmethod
    def add_baddie(_domain_name, _ip_id, _crt_id, _levenstein_dist, _levenstein_matched_keyword, _contained_matched_keyword, _entropy):
        new_baddie = Baddies(domain_name=_domain_name, 
        ip_id=_ip_id, 
        crt_id=_crt_id, 
        levenstein_dist=_levenstein_dist,
        levenstein_matched_keyword=_levenstein_matched_keyword,
        contained_matched_keyword=_contained_matched_keyword,
        entropy=_entropy
        )
        db.session.add(new_baddie)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
        return Baddies.query.filter(Baddies.domain_name == _domain_name).first().id

    @staticmethod
    def add_baddie_td():
        Baddies.add_baddie("g0ogle.com", 1, 1, 1, 'test', 'test', 4)
        Baddies.add_baddie("wekkaa.com", 1, 1, 2, 'test', 'test', 4)

    @staticmethod
    def get_all_baddies():
        return [Baddies.json(b) for b in Baddies.query.all()]