import os
import numpy as np
import pandas as pd

class DatasetHelper(object):
    '''
        这个类是基于某个数据集，并在读取了数据集的基础上，提取一些信息
    '''
    def __init__(self, dataset_path):
        '''
            参数：
                dataset_path表示数据集路径
        '''
        self._path = dataset_path
        self._df = pd.read_csv(dataset_path)

    def get_dataset_size(self):
        '''
            获取文件的大小
        '''
        return os.path.getsize(self._path)

    def get_num_rows(self):
        '''
            获取数据文件中表格的行数
        '''
        return self._df.shape[0]

    def get_columns(self):
        '''
            获取数据文件中的所有列信息，返回一个列表
            {
                name: '' ,
                dtype: '' ,
                type: '', // 'category'或者'numeric'
            }
        '''
        names = list(self._df.columns)
        dtypes = list(map(str, self._df.dtypes))

        column_info = []
        for i in range(len(names)):
            info = {}
            info['name'] = names[i]
            info['dtype'] = dtypes[i]
            info['type'] = 'numeric' if self._is_numeric(names[i]) else 'category'
            column_info.append(info)

        return column_info

    def _is_numeric(self, col_name):
        '''
            判断一列数据是否是numeric类型的
        '''
        return np.issubdtype(self._df[col_name].dtype, np.number)



def test():
    helper = DatasetHelper('../../data/guest/iris.csv')
    print(helper.get_dataset_size())
    print(helper.get_num_rows())
    print(helper.get_columns())

if __name__ == '__main__':
    test()