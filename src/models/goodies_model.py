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
        Goodie.add_goodie("wp")
        Goodie.add_goodie("9gag")
        Goodie.add_goodie("weka")

    @staticmethod
    def get_all_goodies():
        return [Goodie.json(b) for b in Goodie.query.all()]