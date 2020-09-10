from flask import Flask
from extentions.extentions import ma
from app.model import MoviesModel
from marshmallow import fields,validate




class MoviesSchema(ma.SQLAlchemyAutoSchema):

    title = fields.String(required=True, validate=[validate.Length(min=2, max=60)])
    director = fields.String(required=True, validate=[validate.Length(min=2, max=60)])
    language = fields.String(required=True, validate=[validate.Length(min=2, max=60)])
    poster = fields.String(required=True, validate=[validate.Length(min=2, max=300)])
    runtime = fields.String(required=True, validate=[validate.Length(min=2, max=60)])
    year = fields.Integer(required=True)

    class Meta:
        model = MoviesModel
        load_instance = True





