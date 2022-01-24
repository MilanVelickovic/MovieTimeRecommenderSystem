from flask import Flask
from flask_restful import Api, Resource

from recommender import recommend

app = Flask(__name__)
api = Api(app)

class Recommender(Resource):
    def get(self, movieId):
        result = recommend(movieId)
        return {
            "movieId": movieId,
            "recommendation": result
        }

api.add_resource(Recommender, "/recommend/<int:movieId>")

if __name__ == "__main__":
    app.run(debug=True)