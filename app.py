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
city_add_args.add_argument("name", type=str, required=True, help="Please enter text for provice.")
city_add_args.add_argument("temp", type=str, required=True, help="Please enter text for temp.")
city_add_args.add_argument("weather", type=str, required=True, help="Please enter text for weather.")
city_add_args.add_argument("people", type=str, required=True, help="Please enter text for people.")


city_update_args = reqparse.RequestParser()
city_update_args.add_argument("name", type=str, help="Please enter provice for update.")
city_update_args.add_argument("temp", type=str, help="Please enter temp for update.")
city_update_args.add_argument("weather", type=str, help="Please enter weather for update.")
city_update_args.add_argument("people", type=str, help="Please enter people for update.")


# Set Fields
resource_field = {
    "id" : fields.Integer,
    "name" : fields.String,
    "temp" : fields.String,
    "weather" : fields.String,
    "people" : fields.String,
}

class WeatherCity(Resource):
    @marshal_with(resource_field)
    def get(self, city_id):
        result = CityModel.query.filter_by(id=city_id).first()

        if not result:
            abort(404,message="Province is not found")

        return result

    @marshal_with(resource_field)
    def post(self, city_id):
        result = CityModel.query.filter_by(id=city_id).first()
        if result:
            abort(409, message="Province ID is duplicate.")

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

    @marshal_with(resource_field)
    def patch(self, city_id):
        args = city_update_args.parse_args()
        result = CityModel.query.filter_by(id=city_id).first()

        if not result:
            abort(404, message="Province ID is not found.")

        if args["name"]:
            result.name = args["name"]

        if args["temp"]:
            result.temp = args["temp"]

        if args["weather"]:
            result.weather = args["weather"]

        if args["people"]:
            result.people = args["people"]
        
        db.session.commit()
        return result

api.add_resource(WeatherCity,"/weather/<int:city_id>")


if __name__ == "__main__":
    app.run(debug=True)
