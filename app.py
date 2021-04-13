from flask import Flask
from flask_restful import Api, Resource, abort
from flask_sqlalchemy import SQLAlchemy, Model

app = Flask(__name__)

# Database
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///database.db"
api = Api(app)

class CityModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    temp = db.Column(db.String(100), nullable=False)
    weather = db.Column(db.String(100), nullable=False)
    people = db.Column(db.String(100), nullable=False)

    def __repr__(self): # represent
        return f"City(name={name}, temp={temp}, weather={weather}, people={people})"

db.create_all()

"""
mycity = {
    1 : {
        "name" : "chonburi",
        "weather" : "hot",
        "people" : 1000,
    },
    2 : {
        "name" : "rayong",
        "weather" : "very hot",
        "people" : 2000,
    },
    3 : {
        "name" : "bangkok",
        "weather" : "cloud",
        "people" : 3000,
    },
} """


def notfoundCity(city_id):
    if city_id not in mycity:
        abort(404, message="data not found.")

class WeatherCity(Resource):

    def get(self, city_id):
        notfoundCity(city_id)
        return mycity[city_id]

    def post(self, city_id):
        return {"data": "post city id : " + str(city_id)}
        


api.add_resource(WeatherCity,"/weather/<int:city_id>")


if __name__ == "__main__":
    app.run(debug=True)
