import os
import json

from flask_restful import Resource

import service.config as config
from service.common.utils import DatasetHelper


class DatasetMetadata(Resource):

    def post(self, user_id, dataset_name):
        """Create metadata from dataset, 
        including:
            dataset name,
            file size,
            number of rows,
            information of columns.
        Stored as json file.
        """
        helper = DatasetHelper(user_id, dataset_name)
        # Extract meta data.
        try:
            meta = helper.get_meta_data()
        except FileNotFoundError:
            return {}, 400

        # Write file.
        helper.save_meta_data(meta)
        
        return meta, 200

    def get(self, user_id, dataset_name=None):
        """
            Get metadata of dataset.
            If dataset_name is None, it will return user's
            all dataset information.
            Else, it will return a specific dataset's information.
        """
        # Read all dataset names when parameter dataset_name is not given.
        if dataset_name is None:
            files = DatasetHelper.get_dataset_by_user(user_id)
            return files, 200
        helper = DatasetHelper(user_id, dataset_name)
        try:
            meta = helper.get_meta_data(from_file=True)
        except FileNotFoundError:
            return {}, 400

        return meta, 200
    
