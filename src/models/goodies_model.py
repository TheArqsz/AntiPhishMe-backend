import json
import datetime

from db_config import db


class Goodie(db.Model):
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
        new_goodie = Goodie(good_keyword=_good_keyword)
        db.session.add(new_goodie)
        db.session.commit()

    @staticmethod
    def add_goodie_td():
        Goodie.add_goodie("google")
        Goodie.add_goodie("facebook")
        Goodie.add_goodie("onet")
        Goodie.add_goodie("9gag")
        Goodie.add_goodie("weka")
        Goodie.add_goodie("agricole")
        Goodie.add_goodie("santander")
        Goodie.add_goodie("paypal")
        Goodie.add_goodie("dotpay")
        Goodie.add_goodie("ipko")
        Goodie.add_goodie("mbank")
        Goodie.add_goodie("ibiznes24")
        Goodie.add_goodie("jeja")
        Goodie.add_goodie("jbzd")
        Goodie.add_goodie("urlscan")
        Goodie.add_goodie("virustotal")
        Goodie.add_goodie("radom")
        Goodie.add_goodie("bialystok")
        Goodie.add_goodie("sosnowiec")
        Goodie.add_goodie("whitehats")
        Goodie.add_goodie("jsos")
        Goodie.add_goodie("github")
        Goodie.add_goodie("redhat")
        Goodie.add_goodie("epuap")
        Goodie.add_goodie("gmail")
        Goodie.add_goodie("proton")
        Goodie.add_goodie("onedrive")

    @staticmethod
    def get_all_goodies():
        return [Goodie.json(b) for b in Goodie.query.all()]