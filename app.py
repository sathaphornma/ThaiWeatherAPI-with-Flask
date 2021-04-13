from flask import Flask
from flask_restful import Api, Resource, abort, reqparse, marshal_with, fields
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

# Set Fields
resource_field = {
    "id" : fields.Integer,
    "name" : fields.String,
    "temp" : fields.String,
    "weather" : fields.String,
    "people" : fields.String,
}


def notfoundCity(city_id):
    if city_id not in mycity:
        abort(404, message="province not found.")

class WeatherCity(Resource):
    @marshal_with(resource_field)
    def get(self, city_id):
        notfoundCity(city_id)
        return mycity[city_id]

    @marshal_with(resource_field)
    def post(self, city_id):
        args = city_add_args.parse_args()
        city = CityModel(
            id=city_id, 
            name=args["name"], 
            temp=args["temp"], 
            weather=args["weather"], 
            people=args["people"]
        )

        db.session.add(city)
        db.session.commit()
        return city,201
        


api.add_resource(WeatherCity,"/weather/<int:city_id>")


if __name__ == "__main__":
    app.run(debug=True)
