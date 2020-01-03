import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from service.common.dataset_helper import DatasetHelper


class DrawerHelper(object):

    def __init__(self, user_id, dataset_name):
        """

        """
        self._dataset_helper = DatasetHelper(user_id, dataset_name)
        
    def draw_distribution_histgram(self, columns):
        """Draw a distribution histgram.
        Args:
            columns: columns of x-axis.
        Return:
            A config object describe how to draw histgram.
        """
        cols = self._dataset_helper.df[columns]
        ax = sns.distplot(cols, kde = False)
        x_width = ax.patches[0].get_width()
        x_axis = [(h.get_x(), h.get_x() + x_width) for h in ax.patches]
        heights = [h.get_height() for h in ax.patches]
        return {
            'chart_type': 'distribution_histgram',
            'data': {
                'x_axis': x_axis,
                'heights': heights
            }
        }
        
    