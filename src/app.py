from flask import Flask
import flask
from flask_restful import Api, Resource
from flask_cors import CORS

from cbrs import recommend

app = Flask(__name__)
api = Api(app)
CORS(app)

class Recommender(Resource):
    def get(self, movieId: int):
        result = recommend(movieId)
        response = flask.jsonify({
            "movieId": movieId,
            "recommendation": result
        })
        response.headers.add("Access-Control-Allow-Origin", '*')
        response.headers.add("Access-Control-Allow-Headers", 'Content-Type,Authorization')
        response.headers.add("Access-Control-Allow-Methods", 'GET, POST')
        
        return response

api.add_resource(Recommender, "/recommend/<int:movieId>")

if __name__ == "__main__":
    app.run(debug=True)