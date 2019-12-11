from flask_restful import Resource
from werkzeug.utils import secure_filename
import os, json
import service.config as config
from service.common.utils import DatasetHelper

class DatasetMetadata(Resource):

    def post(self, user_id, dataset_name):
        '''
            新建数据集的元数据，包括数据集名、大小、行数、列 等
            用json文件存储
        '''
        dataset_path = self._check_and_get_dataset_path(dataset_name)
        if not dataset_path:
            return {}, 400

        # 抽取元数据
        meta = {}
        meta['name'] = dataset_name
        helper = DatasetHelper(dataset_name)
        meta['size'] = helper.get_file_size()
        meta['num_rows'] = helper.get_num_rows()
        meta['columns'] = helper.get_columns()

        # 写入文件
        with open(self._get_dataset_metadata_filename(dataset_path), 'w') as f:
            json.dump(meta, f)
        
        return meta, 200


    def get(self, user_id, dataset_name):
        '''
            获取数据集的元数据，包括数据集名、大小、行数、列 等
        '''
        dataset_path = self._check_and_get_dataset_path(dataset_name)
        if not dataset_path or \
            not os.path.exists(self._get_dataset_metadata_filename(dataset_path)):
            return {}, 400

        # 读取元数据文件
        meta = {}
        with open(self._get_dataset_metadata_filename(dataset_path)) as f:
            meta = json.load(f)

        return meta, 200


    def _get_dataset_metadata_filename(self, dataset_name):
        '''
            根据数据文件名，得到元数据文件名
        '''
        return dataset_path + '.meta'

    def _check_and_get_dataset_path(self, dataset_name):
        '''
            检查数据文件是否存在
            若存在，则返回路径名
            若不存在，返回None
        '''
        root = os.path.join(config.UPLOAD_FOLDER, user_id)
        dataset_name = secure_filename(dataset_name)
        dataset_path = os.path.join(root, dataset_name)

        # 检查数据文件是否存在
        if os.path.exists(root) and not os.path.exists(dataset_path):
            return None
        return dataset_path