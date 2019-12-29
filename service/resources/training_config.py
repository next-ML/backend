from flask_restful import Resource
from flask import request

from service.common.utils import TrainingTaskHelper


class TrainingConfig(Resource):
    
    def post(self, user_id, task_name):
        config_data = request.get_json()
        keys_to_check = set(['user_id', 
                             'dataset_name', 
                             'model_type',
                             'label_columns',
                             'feature_columns',
                             'time_limit',
                             'max_trial'])
        # Check parameters's integrity.
        if set(config_data.keys()) != keys_to_check:
            return {}, 400
        
        helper = TrainingTaskHelper(user_id, task_name)
        helper.save_config_file(config_data)
        return config_data, 200
        
    def get(self, user_id, task_name):
        helper = TrainingTaskHelper(user_id, task_name)
        config_data = helper.read_config_file()
        if config_data is None:
            return {}, 400
        return config_data, 200

