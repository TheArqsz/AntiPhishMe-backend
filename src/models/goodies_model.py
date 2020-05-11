import json
import datetime
import sqlalchemy
import logging as log

from db_config import db


class Goodies(db.Model):
    __tablename__ = 'goodies'
    id = db.Column(db.Integer(), primary_key=True)
    good_keyword = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {
            'good_keyword': self.good_keyword
            }

    @staticmethod
    def add_goodie(
        _good_keyword
        ):
        new_goodie = Goodies(good_keyword=_good_keyword)
        db.session.add(new_goodie)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError as e:
            log.error(e)
            db.session.rollback()
        try:
            return Goodies.query.filter(Goodies.good_keyword == _good_keyword).first().id
        except AttributeError as e:
            log.error(e)
            return -1

    @staticmethod
    def add_goodie_td():
        Goodies.add_goodie("google")
        Goodies.add_goodie("facebook")
        Goodies.add_goodie("onet")
        Goodies.add_goodie("9gag")
        Goodies.add_goodie("weka")
        Goodies.add_goodie("agricole")
        Goodies.add_goodie("santander")
        Goodies.add_goodie("paypal")
        Goodies.add_goodie("dotpay")
        Goodies.add_goodie("ipko")
        Goodies.add_goodie("mbank")
        Goodies.add_goodie("ibiznes24")
        Goodies.add_goodie("jeja")
        Goodies.add_goodie("jbzd")
        Goodies.add_goodie("urlscan")
        Goodies.add_goodie("virustotal")
        Goodies.add_goodie("radom")
        Goodies.add_goodie("bialystok")
        Goodies.add_goodie("sosnowiec")
        Goodies.add_goodie("whitehats")
        Goodies.add_goodie("jsos")
        Goodies.add_goodie("github")
        Goodies.add_goodie("redhat")
        Goodies.add_goodie("epuap")
        Goodies.add_goodie("gmail")
        Goodies.add_goodie("proton")
        Goodies.add_goodie("onedrive")

    @staticmethod
    def get_all_goodies():
        return [Goodies.json(b) for b in Goodies.query.all()]