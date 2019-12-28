from flask import Flask
from flask_restful import Api

from service.resources.dataset import Dataset
from service.resources.dataset_metadata import DatasetMetadata
from service.resources.training_config import TrainingConfig


app = Flask(__name__)
api = Api(app)

api.add_resource(Dataset, '/<string:user_id>/dataset/<string:dataset_name>',
                          endpoint='dataset')
api.add_resource(DatasetMetadata, '/<string:user_id>/dataset/<string:dataset_name>/meta',
                                  '/<string:user_id>/dataset/meta',
                                  endpoint='dataset_metadata')
api.add_resource(TrainingConfig, '/<string:user_id>/<string:task_name>/training_config',
                                  endpoint='training_config')
