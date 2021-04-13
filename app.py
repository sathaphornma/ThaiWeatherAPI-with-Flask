from flask import Flask
from flask_restful import Api, Resource, abort, reqparse
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)

# Create Database
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
api = Api(app)

# Design Database
class CityModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.String(100), nullable=False)
    weather = db.Column(db.String(100), nullable=False)
    people = db.Column(db.String(100), nullable=False)

    def __repr__(self): # represent
        return f"City(name={name}, temp={temp}, weather={weather}, people={people})"

db.create_all()

# Request Parser
city_add_args = reqparse.RequestParser()
city_add_args.add_argument("name", type=str, required=True, help="please enter text for provice.")
city_add_args.add_argument("temp", type=str, required=True, help="please enter text for temp.")
city_add_args.add_argument("weather", type=str, required=True, help="please enter text for weather.")
city_add_args.add_argument("people", type=str, required=True, help="please enter text for people.")

mycity = {
    "chonburi" : {
        "name" : "chonburi",
        "weather" : "hot",
        "people" : 1000,
    },
    "rayong" : {
        "name" : "rayong",
        "weather" : "very hot",
        "people" : 2000,
    },
    "bangkok" : {
        "name" : "bangkok",
        "weather" : "cloud",
        "people" : 3000,
    },
}


def notfoundCity(name):
    if name not in mycity:
        abort(404, message="province not found.")

class WeatherCity(Resource):

    def get(self, name):
        notfoundCity(name)
        return mycity[name]

    def post(self, name):
        args = city_add_args.parse_args()
        return args
        


api.add_resource(WeatherCity,"/weather/<string:name>")


if __name__ == "__main__":
    app.run(debug=True)
