import os
from sqlalchemy import Column, String, Integer, create_engine,Date
from flask_sqlalchemy import SQLAlchemy
import json
from datetime import date
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()
    

def db_initiate():
    actor=Actors(name="Ganesh",age=22,Gender="Male")
    movie=Movie(title='Avengers',release_date='2014-07-12')
    performance=Performance.insert().values(Movie_id=movie.id,Actor_id=actor.actor_id,actor_fee=50000.00)
    actor.insert()
    movie.insert()
    db.session.execute(performance)
    db.session.commit()

Performance = db.Table('Performance', db.Model.metadata,
    db.Column('Movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('Actor_id', db.Integer, db.ForeignKey('actors.actor_id')),
    db.Column('actor_fee', db.Float)
)


class Movie(db.Model):
    __tablename__='movies'
    id=Column(Integer,primary_key=True)
    title=Column(String)
    release_date=Column(Date)
    actors = db.relationship('Actors', secondary=Performance, backref=db.backref('performances', lazy='joined'))

 
    def __init__(self,title,release_date):
        self.title=title
        self.release_date=release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def long(self):
        return {
            'id':self.id,
            'title':self.title,
            'release_date':self.release_date
        }

class Actors(db.Model):
    __tablename__='actors'
    actor_id=Column(Integer,primary_key=True)
    name=Column(String)
    age=Column(Integer)
    Gender=Column(String)
  

    def __init__(self,name,age,Gender):
        self.name=name
        self.age=age
        self.Gender=Gender

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def long(self):
        return {
            'id':self.actor_id,
            'actor_name':self.name,
            'actor_age':self.age,
            'gender':self.Gender
        }


