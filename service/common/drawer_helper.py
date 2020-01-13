import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.cbook import boxplot_stats
from sklearn.linear_model import LinearRegression

from service.common.dataset_helper import DatasetHelper


class DrawerHelper(object):

    def __init__(self, user_id, dataset_name, target_col='jinpu_ug_ml'):
        """

        """
        self._dataset_helper = DatasetHelper(user_id, dataset_name)
        self._target_col = target_col

        
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
        
    def draw_covariance_heatmap(self):
        """Draw a heatmap whose content is covariance of features.
        
        Firstly, the algorithm will select top k features to draw.
        Then calculate the covariance matrix between selected features.
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
        
    def draw_feature_importance(self):
        """Draw a bar plot represent feature importance.
        
        First train a linear regression model.
        Then use weight to represent the feature importance.
        """
        model = LinearRegression()
        df = self._dataset_helper.df
        y = df[self._target_col]
        x = df.drop(self._target_col, axis=1)
        model.fit(x, y)
        coef = list(map(abs, model.coef_))
        importance = zip(list(x.columns), coef)
        importance = sorted(importance, key=lambda x: abs(x[1]), reverse=True)
        return {
            'features': [v[0] for v in importance],
            'weights': [v[1] for v in importance]
        }
        
    def draw_boxing_chart(self):
        """Draw a boxplot present relation between top k features and target.
        
        Return a list of boxplot configuration.
        """
        # Select only top k features.
        k = 4
        
        columns = self._top_k_importance(self._filter_category(), k)
        # print(self._dataset_helper.df.shape)
        box_setting = []
        for col in columns:
            plt.clf()
            df = self._dataset_helper.df[[col, self._target_col]]
            stats = boxplot_stats(df, labels=[col])
            print(stats)
            sns.boxplot(x=col, y=self._target_col, data=self._dataset_helper.df)
            plt.show()
        
    def _filter_numeric(self):
        columns = self._dataset_helper.df.columns
        return [col for col in columns if self._dataset_helper.is_numeric(col)]
      
    def _filter_category(self):
        columns = self._dataset_helper.df.columns
        return [col for col in columns if not self._dataset_helper.is_numeric(col)]
        
    def _top_k_importance(self, columns, k):
        # return columns[1:k+1]
        return ['charge_of_the_rest', 'negative_charge', 'ph_number', 'length']

