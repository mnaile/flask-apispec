from flask import Flask, request, jsonify, Response
from app.model import MoviesModel 
from app.serializer import MoviesSchema
from app_init.app_factory import create_app
from marshmallow import ValidationError
from http import HTTPStatus
from webargs import fields
import json
from flask_apispec import use_kwargs, marshal_with,FlaskApiSpec, MethodResource

import os

settings_name = os.getenv("settings")
app = create_app(settings_name)

@app.route("/allmovies",methods=["GET"])
@use_kwargs({'title': fields.Str(),
            'director': fields.Str(),
            'language': fields.Str(),
            'poster': fields.Str(),
            'runtime': fields.Str(),
            'year': fields.Integer()
})
@marshal_with(MoviesSchema(many=True))
def list_movies(**kwargs):
    return MoviesModel.query.filter_by(**kwargs).all()




@marshal_with(MoviesSchema)
class MovieResource(MethodResource):

    def get(self, movie_id):
        return MoviesModel.query.filter_by(id=movie_id).first()



class MovieDeleteResource(MethodResource):
    def delete(self, movie_id, **kwargs):
        movie = MoviesModel.query.filter_by(id=movie_id).first()
        if movie:
            movie.delete_from_db()
            return Response(json.dumps({'result': True}), status=200, mimetype="application/json")
        return Response(json.dumps({'result': False}),status=404,mimetype="application/json")

@use_kwargs({'title': fields.Str(),
            'director': fields.Str(),
            'language': fields.Str(),
            'poster': fields.Str(),
            'runtime': fields.Str(),
            'year': fields.Integer()
})
class MovieUpdateResource(MethodResource):
    def put(self, movie_id,**kwargs):
        try: 
            movie = MoviesModel.query.filter_by(id=movie_id).first()
            if  movie:
                new_data = request.get_json()
                print(new_data)
        
                movie.update_db(**new_data)
                return Response(json.dumps({'result': True}), status=200, mimetype="application/json")

        except ValidationError as err:
            return Response(err.messages, status=500, mimetype="application/json")
        
        return Response(json.dumps({'result': False}), status=404, mimetype="application/json")

       


docs = FlaskApiSpec(app,document_options=False)
docs.register(target=list_movies)

app.add_url_rule('/movies', view_func=MovieResource.as_view('Movie'))
docs.register(MovieResource, endpoint='Movie')
app.add_url_rule('/movies/<int:movie_id>', view_func=MovieDeleteResource.as_view('DeleteMovie'))
docs.register(MovieDeleteResource,endpoint='DeleteMovie')
app.add_url_rule('/movies/<int:movie_id>', view_func=MovieUpdateResource.as_view('UpdateMovie'))
docs.register(MovieUpdateResource,endpoint='UpdateMovie')




@app.route('/movie', methods=["POST"])
def create_movie():
    data = request.get_json()
    try:
        data_schema = MoviesSchema().load(data)
        data_schema.save_db()
    except ValidationError as err:
        return jsonify(err.messages),HTTPStatus.BAD_REQUEST
    return MoviesSchema().jsonify(data_schema),HTTPStatus.OK



@app.route('/movies', methods=["POST"])
def get_movies():
    # print(request.get_json())
    data_title = MoviesModel.query.filter_by(title=request.get_json().get("title")).all()
    if data_title:
        data_schema = MoviesSchema().dump(data_title,many=True)
        return MoviesSchema().jsonify(data_schema,many=True)

    data_director = MoviesModel.query.filter_by(director=request.get_json().get("director")).all()
    if data_director:
        data_schema = MoviesSchema().dump(data_director, many=True)
        return MoviesSchema().jsonify(data_schema,many=True)

    data_year = MoviesModel.query.filter_by(year=request.get_json().get("year")).all()
    if data_year:
        data_schema = MoviesSchema().dump(data_year, many=True)
        return MoviesSchema().jsonify(data_schema,many=True)
    
    return jsonify(msg="Melumat yoxdur"), HTTPStatus.NOT_FOUND
    
        
