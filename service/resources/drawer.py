
from flask_restful import Resource
from flask import request

from service.common.drawer_helper import DrawerHelper


class Drawer(Resource):
    """
    """
    
    def post(self, user_id):
        """
        """
        data = request.get_json()
        check_key = set(['dataset_name', 
                         'chart_type', 
                         'row_attrs', 
                         'columns_attrs',
                         'color_attr',
                         'size_attr',
                         'style_attr'])
        if check_key != set(data.keys()):
            return {}, 400

        if data['chart_type'] == 'distribution':
            attrs = [attr['name'] for attr in data['row_attrs']]
            config = self.draw_distribution(user_id,
                                            data['dataset_name'], 
                                            attrs)
        
        return config, 200
    
    def draw_distribution(self, user_id, dataset_name, row_attrs):
        drawer_helper = DrawerHelper(user_id, dataset_name)
        config = drawer_helper.draw_distribution_histgram(row_attrs)
        return config
        
