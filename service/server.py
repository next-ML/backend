from flask import Flask
from flask_restful import Api
from service.resources.dataset import Dataset


app = Flask(__name__)
api = Api(app)

api.add_resource(Dataset, '/<string:user_id>/dataset')