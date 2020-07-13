import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from auth import AuthError, requires_auth
from models import db_drop_and_create_all,setup_db,Movie,Actors
from config import pagination

ROWS_PER_PAGE = pagination['pages']
def create_app(test_config=None):
    app=Flask(__name__)
    
    setup_db(app)
    
    CORS(app)
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    #db_drop_and_create_all()

    #paginating output
    def paginate_resullts(request,selection):
        page = request.args.get('page', 1, type=int)
        start =  (page - 1) * ROWS_PER_PAGE
        end = start + ROWS_PER_PAGE
        formated = [object_name.long() for object_name in selection]
        return formated[start:end]

    #Gets actors
    @app.route('/actors',methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        #querying database
        all_actors=Actors.query.all()
        #if all_actors is empty
        if len(all_actors)==0:
            abort(404)

        
    
        actors=paginate_resullts(request,all_actors)

        

        return jsonify(
            {
            "success":True,
            "actors":actors
            }
        )

    #gets movies
    @app.route('/movies',methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        #querying database
        all_movies=Movie.query.all()
        #if no records found
        if len(all_movies)==0:
            abort(404)

        movies=paginate_resullts(request,all_movies)

        return jsonify(
            {
            "success":True,
            "movies":movies
            }
        )

    #deletes actor with given id 
    @app.route('/actors/<int:id>',methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(*args,**kwargs):
        #gets the id given from url
        id=kwargs['id']
        #searches for actor with given id 
        actor=Actors.query.filter_by(actor_id=id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()
        except:
            abort(500)

        return jsonify({
            "success":True,
            "delete":id
        })

    #deletes the movie with given id
    @app.route('/movies/<int:id>',methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(*args,**kwargs):
        #gets the id given from url
        id=kwargs['id']
        #searches for movie with given id
        movie=Movie.query.filter_by(id=id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()
        except:
            abort(500)

        return jsonify({
            "success":True,
            "delete":id
        })
    

    #inserts actor into database
    @app.route('/actors',methods=['POST'])
    @requires_auth('post:actor')
    def save_actor(jwt):
        #gets the body from request
        body=request.get_json()

        name=body['name']
        #name is not given
        if name is None:
            abort(422)
                
        age=body['age']
        #age is not given
        if age is None:
            abort(422)
        
        Gender=body['Gender']
        #gender is not given 
        if Gender is None:
            abort(422)

        actor=Actors(name=name,age=age,Gender=Gender)
    
        try:
            actor.insert()
        except:
            abort(500)

        return jsonify({
            'success':True,
            'actor_id':actor.actor_id
        })


    #inserts movie into database
    @app.route('/movies',methods=['POST'])
    @requires_auth('post:movie')
    def save_movie(jwt):
        #gets body from request
        body=request.get_json()
        title=body['title']
        #title not given
        if title is None:
            abort(422)

        release_date=body['release_date']
        
        #release_date not given
        if release_date is None:
            abort(422)

        movie=Movie(title=title,release_date=release_date)

        try:
            movie.insert()
        except:
            abort(500)

        return jsonify(
            {
            'success':True,
            'movie_id':movie.id
            }
        )

    #updates actor
    @app.route('/actors/<int:id>',methods=['PATCH'])
    @requires_auth('update:actor')
    def update_actor(*args, **kwargs):
        #gets id from url
        id=kwargs['id']
    
        actor_by_id=Actors.query.filter_by(actor_id=id).one_or_none()
    
        if actor_by_id is None:
            abort(404)
        #gets the body from request
        body=request.get_json()
        
        name=body['name']
        #name is not given
        if name is None:
            abort(422)
                
        age=body['age']
        #age is not given
        if age is None:
            abort(422)
        
        Gender=body['Gender']
        #gender is not given 
        if Gender is None:
            abort(422)

        actor_by_id.name=body["name"]
        actor_by_id.age=body["age"]
        actor_by_id.Gender=body["Gender"]

        try:
            actor_by_id.update()
        except:
            abort(500)
        return jsonify({
            "success":True,
            "actor_id":actor_by_id.actor_id
        })
    

    #update movies
    @app.route('/movies/<int:id>',methods=['PATCH'])
    @requires_auth('update:movie')
    def update_movie(*args, **kwargs):
        #gets id from url
        id=kwargs['id']

        movie_by_id=Movie.query.filter_by(id=id).one_or_none()

        if movie_by_id is None:
            abort(404)
        #gets body from request
        body=request.get_json()

        if body["title"] is None:
            abort(422)

        if body["release_date"] is None:
            abort(422)
        
        movie_by_id.title=body["title"]

        movie_by_id.release_date=body["release_date"]
    
        try:
            movie_by_id.update()
        except:
            abort(500)

        return jsonify({
            "success":True,
            "movie_id":movie_by_id.id
        })



    #error 422
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

    #error 404
    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

    #Authentication
    @app.errorhandler(AuthError)
    def auth_error_occurence(ex):
        res = jsonify(ex.error)
        res.status_code = ex.status_code
        return res

    return app


app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)



