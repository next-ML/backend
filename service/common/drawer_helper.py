import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from service.common.dataset_helper import DatasetHelper


class DrawerHelper(object):

    def __init__(self, user_id, dataset_name, target_col='jinpu_ug_ml'):
        """

        """
        self._dataset_helper = DatasetHelper(user_id, dataset_name)
        self._target_col = target_col
        
    def draw_covariance_heatmap(self):
        """Draw a heatmap whose content is covariance of features.
        
        Firstly, the algorithm will select top k features to draw.
        """
        # Only select top k.
        k = 12
        
        corrmat = self._dataset_helper.df.corr()
        cols = corrmat.nlargest(k, self._target_col)[self._target_col].index
        cm = np.corrcoef(self._dataset_helper.df[cols].values.T)
        return {
            'columns': list(cols),
            'covariance_matrix': cm.tolist()
        }

        
    def draw_distribution_histgram(self, columns):
        """Draw a distribution histgram.
        Args:
            columns: columns of x-axis.
        Return:
            A config object describe how to draw histgram.
        """
        
        if not columns:
            # Return a zero bar if column is null.
            x_axis = [0, 0],
            heights = [0]
        else:
            if len(columns) > 1:
                columns = columns[0]
            plt.clf()
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
        
    