import os

from flask_restful import Resource
from flask import request
from werkzeug.utils import secure_filename

import service.config as config
from service.common.utils import DatasetHelper


class Dataset(Resource):
    
    # Only allowed csv file currently.
    ALLOWED_EXTENSIONS = {'csv'}

    @staticmethod
    def allowed_file(filename):
        """Check file extension."""
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Dataset.ALLOWED_EXTENSIONS

    def post(self, user_id, dataset_name):
        """Upload a dataset file."""
        # Check request correctness.
        if 'file' not in request.files:
            return {}, 400
        file = request.files['file']
        if file.filename == '':
            return {}, 400
        if not file or \
            not Dataset.allowed_file(file.filename):
            return {}, 400
        
        directory = os.path.join(config.DATA_FOLDER, 
                                 user_id,
                                 'dataset')

        # If directory not exist now, create recursively.
        if not os.path.isdir(directory):
            os.makedirs(directory, exist_ok=True)

        filename = secure_filename(file.filename)
        filepath = os.path.join(directory, filename)
        file.save(filepath)

        # Analyse and save meta data automatically.
        helper = DatasetHelper(user_id, dataset_name)
        meta = helper.get_meta_data()
        helper.save_meta_data(meta)
        return meta, 200
    
    def get(self, user_id, dataset_name):
        """Get raw data from data file."""
        helper = DatasetHelper(user_id, dataset_name)
        raw_data = helper.get_raw_data()
        return {'data': raw_data}, 200

