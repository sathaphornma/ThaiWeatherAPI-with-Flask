from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

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
} 

class WeatherCity(Resource):

    def get(self, city_id):
        return mycity[city_id]

    def post(self, city_id):
        return {"data": "post data : " + str(city_id)}
        


api.add_resource(WeatherCity,"/weather/<int:city_id>")


if __name__ == "__main__":
    app.run(debug=True)
