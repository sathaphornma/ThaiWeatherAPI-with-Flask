from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class WeatherCity(Resource):

    def get(self):
        return {"data":"hello"}




api.add_resource(WeatherCity,"/weather")


if __name__ == "__main__":
    app.run(debug=True)
