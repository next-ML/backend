
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
                         'chart_type'])
        if check_key > set(data.keys()):
            return {}, 400

        drawer_helper = DrawerHelper(user_id, data['dataset_name'])
        
        if data['chart_type'] == 'distribution':
            if 'row_attrs' not in data:
                return {}, 400
            attrs = [attr['name'] for attr in data['row_attrs']]
            draw_setting = self.draw_distribution(drawer_helper, attrs)
        elif data['chart_type'] == 'covariance':
            draw_setting = self.draw_covariance(drawer_helper)
        elif data['chart_type'] == 'weight':
            draw_setting = self.draw_weight(drawer_helper)
        elif data['chart_type'] == 'boxing':
            draw_setting = self.draw_boxing(drawer_helper)
        elif data['chart_type'] == 'scatter':
            draw_setting = self.draw_scatter(drawer_helper)
        
        return draw_setting, 200
    
    def draw_distribution(self, drawer_helper, row_attrs):
        draw_setting = drawer_helper.draw_distribution_histgram(row_attrs)
        return draw_setting
      
    def draw_covariance(self, drawer_helper):
        draw_setting = drawer_helper.draw_covariance_heatmap()
        return draw_setting
      
    def draw_weight(self, drawer_helper):
        draw_setting = drawer_helper.draw_feature_importance()
        return draw_setting
      
    def draw_boxing(self, drawer_helper):
        draw_setting = drawer_helper.draw_boxing_chart()
        return draw_setting
      
    def draw_scatter(self, drawer_helper):
        draw_setting = drawer_helper.draw_scatter_chart()
        return draw_setting
        
