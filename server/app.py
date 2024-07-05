#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Newsletter

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Home(Resource):
    
    def get(self):

        response = {
            "message": "Welcome to the Newsletter RESTful API",
        }

        return response, 200

api.add_resource(Home, '/')

class Newsletters(Resource):
   
    def get(self):
        news_letters = Newsletter.query.all()
        return [n.to_dict() for n in news_letters], 200


    def post(self):
        new_record = Newsletter(
            title=request.form.get('title'),
            body=request.form.get('body')
        )

        db.session.add(new_record)
        db.session.commit()
        
        return new_record.to_dict(), 200

api.add_resource(Newsletters, '/newsletters')

class NewsletterById(Resource):
    
    def get(self, id):

        newsletter = Newsletter.query.fitler(Newsletter.id == id).first()

        return newsletter.to_dict(), 200

api.add_resource(NewsletterById, '/newsletters/<int:id>')



if __name__ == '__main__':
    app.run(port=5555, debug=True)
