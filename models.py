import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
import json

# make sure you create a database named hello in psql
database_name = "hello"
database_path = 'postgresql://postgres:123456@localhost:5432/{}'.format(
    database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Greeting
'''


class Greeting(db.Model):
    __tablename__ = 'greetings'

    id = Column(Integer, primary_key=True)
    lang = Column(String)
    greeting = Column(String)

    def __init__(self, lang, greeting):
        self.lang = lang
        self.greeting = greeting
    def update(self):
        db.session.commit()
    def insert(self):
        db.session.add(self)
        db.session.commit()
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    def format(self):
        return {
            'lang': self.lang,
            'greeting': self.greeting,
        }
