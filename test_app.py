from app import create_app
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from config import bearer_tokens
from sqlalchemy import desc
from datetime import date
from models import setup_db, db_drop_and_create_all, Actors, Movie, Performance, db_drop_and_create_all,database_path


casting_assistant_auth_header = {
    'Authorization': bearer_tokens["casting_assistant"]
}

casting_director_auth_header = {
    'Authorization': bearer_tokens["casting_director"]
}

executive_producer_auth_header = {
    'Authorization': bearer_tokens["executive_producer"]
}



class AgencyTestCase(unittest.TestCase):
    """This class represents the agency test case"""

    def setUp(self):

        """Define test variables and initialize app."""
        self.app = create_app()

        self.client = self.app.test_client
        
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    #----------------------------#
    #Testing for Casting Assistant
    #----------------------------#

    def test_create_new_actor(self):
        actor={"name":"John","age":24,"Gender":'Male'}
        res=self.client().post('/actors',json=actor,headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
     
    def test_create_actor_401_error(self):
        actor={"name":"John","age":24,"Gender":"Male"}
        res=self.client().post('/actors',json=actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'],'Authorization header is expected.')
    
    def test_create_actor_422_error(self):
        actor={"name":None,"age":24,"Gender":"Female"}
        res=self.client().post('/actors',json=actor,headers=casting_director_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"],"unprocessable")        
    
#----------------------------------------------------------------------------#
# Tests for /actors GET
#----------------------------------------------------------------------------#



    def test_get_all_actors(self):
        """Test GET all actors."""
        res=self.client().get('/actors',headers=casting_assistant_auth_header)
        data=json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['actors']),1)
    
    def test_get_all_actors_401_error(self):
        res=self.client().get('/actors')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'],'Authorization header is expected.')
#----------------------------------------------------------------------------#
# Tests for /actors PATCH
#----------------------------------------------------------------------------#


    def test_edit_actor(self):
        """Test PATCH all actors."""
        actor={"name":"Sujana","age":30,"Gender":"Female"}
        res=self.client().patch('/actors/1',json=actor,headers=casting_director_auth_header)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data["actor_id"],1)

    def test_edit_actor_404_error(self):
        actor={"name":"Sujana","age":30,"Gender":"Female"}
        res=self.client().patch('/actors/1000',json=actor,headers=casting_director_auth_header)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_edit_actor_422_error(self):
        actor={"name":None,"age":30,"Gender":"Female"}
        res=self.client().patch('/actors/1',json=actor,headers=casting_director_auth_header)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"],"unprocessable")        

#----------------------------------------------------------------------------#
# Tests for /actors DELETE
#----------------------------------------------------------------------------#
    def test_delete_actor_401_error(self):
        res=self.client().delete('/actors/1')
        data=json.loads(res.data)
        self.assertEqual(data['description'],'Authorization header is expected.')
        self.assertEqual(res.status_code, 401)

    def test_delete_actor_404_error(self):
        res=self.client().delete('/actors/1000',headers=casting_director_auth_header)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"],"resource not found")

    def test_delete_actor(self):
        actor={"name":"Mary","age":26,"Gender":'Female'}
        res=self.client().post('/actors',json=actor,headers=casting_director_auth_header)
        data = json.loads(res.data)
        
        id=str(data["actor_id"])
        res=self.client().delete('/actors/'+id,headers=casting_director_auth_header)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])


#----------------------------------------------------------------------------#
# Tests for /movies POST
#----------------------------------------------------------------------------#
    def test_create_new_movie(self):
        movie={"title":"XMEN Volvarine","release_date":"2017-08-13"}
        res=self.client().post('/movies',json=movie,headers=executive_producer_auth_header)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
     
    def test_create_movie_422_error(self):
        movie={"title":"XMEN Volvarine","release_date":None}
        res=self.client().post('/movies',json=movie,headers=executive_producer_auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"],"unprocessable")        
    
    def test_create_movie_401_error(self):
        movie={"title":"XMEN Volvarine","release_date":"2017-08-13"}
        res=self.client().post('/movies',json=movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'],'Authorization header is expected.')




#----------------------------------------------------------------------------#
# Tests for /movies GET
#----------------------------------------------------------------------------#
    def test_get_all_movies(self):
        res=self.client().get('/movies',headers=casting_assistant_auth_header)
        data=json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['movies']),1)
    
    def test_get_all_movies_401_error(self):
        res=self.client().get('/movies')
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'],'Authorization header is expected.')
    
#----------------------------------------------------------------------------#
# Tests for /movies PATCH
#----------------------------------------------------------------------------#

    def test_edit_movies(self):
        movie={"title":"Avengers End Game","release_date":"2019-05-14"}
        res=self.client().patch('/movies/1',json=movie,headers=executive_producer_auth_header)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(data["movie_id"],1)

    def test_edit_movie_404_error(self):
        movie={"title":"Avengers End Game","release_date":"2019-05-14"}
        res=self.client().patch('/movies/100',json=movie,headers=executive_producer_auth_header)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 404)        
        self.assertEqual(data["message"],"resource not found")
    
    def test_edit_movie_401_error(self):
        movie={"title":"Avengers End Game","release_date":"2019-05-14"}
        res=self.client().patch('/movies/100',json=movie)
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['description'],'Authorization header is expected.')

    def test_edit_movie_422_error(self):
        movie={"title":None,"release_date":"2019-05-14"}
        res=self.client().patch('/movies/1',json=movie,headers=executive_producer_auth_header)
        data=json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["message"],"unprocessable")



#----------------------------------------------------------------------------#
# Tests for /movies DELETE
#----------------------------------------------------------------------------#

    def test_delete_movie_401_error(self):
        res=self.client().delete('/actors/1')
        data=json.loads(res.data)
        self.assertEqual(data['description'],'Authorization header is expected.')
        self.assertEqual(res.status_code, 401)

    def test_delete_movie_404_error(self):
        res=self.client().delete('/actors/1000',headers=casting_director_auth_header)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["message"],"resource not found")
    
    def test_delete_movie(self):
        movie={"title":"Bigboss","release_date":"2017-06-16"}
        res=self.client().post('/movies',json=movie,headers=executive_producer_auth_header)
        data=json.loads(res.data)
        id=str(data["movie_id"])
        res=self.client().delete('/movies/'+id,headers=executive_producer_auth_header)
        data=json.loads(res.data)
        self.assertEqual(res.status_code,200)
        self.assertEqual(int(id),data["delete"])
        