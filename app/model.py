from flask import Flask
from extentions.extentions import db

class MoviesModel(db.Model):

    id = db.Column(db.Integer(), primary_key = True)
    
    title = db.Column(db.String(), nullable=False)
    director = db.Column(db.String(), nullable=False)
    language = db.Column(db.String(), nullable=False)
    poster = db.Column(db.String(), nullable=False)
    runtime = db.Column(db.String(), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    
    def save_db(self):
        db.session.add(self)
        db.session.commit()
        
    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_db(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.save_db()












