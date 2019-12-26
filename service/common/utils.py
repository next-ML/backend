import os
import json
import numpy as np
import pandas as pd

from werkzeug.utils import secure_filename

import service.config as config


class DatasetHelper(object):
    """This class ecapsulates operations over dataset.
    """
    
    def __init__(self, user_id, dataset_name):
        """
        Args:
            user_id: dataset this belongs to whom.
            dataset_name: name of dataset.
        """
        self.dataset_root = os.path.join(config.UPLOAD_FOLDER, 
                                         user_id,
                                         'dataset')
        dataset_path = self._get_dataset_path(user_id, dataset_name)
        self._user_id = user_id
        self._dataset_name = dataset_name
        self._dataset_path = dataset_path
        self._df = pd.read_csv(dataset_path)
    
    def get_meta_data(self, from_file=False):
        """Extract meta data.
        Args:
            from_file: if True, read metadata from json file,
                else extract metadata from original dataset.
        """
        meta = {}
        if from_file:
            with open(self._meta_file_path) as f:
                meta = json.load(f)
        else:
            meta['name'] = self._dataset_name
            meta['size'] = self._dataset_size
            meta['num_rows'] = self._num_rows
            meta['columns'] = self._columns
            
        return meta
    
    def get_raw_data(self):
        """Read and return raw 2-dimension data structure from dataset.
        For example:
        [
    ​		["1", 2019, 30.5],
    ​		["2", 2018, 50.3],
    ​		["3", 2020, 19.0],
        ​]
        """
        raw_data = self._df.values.tolist()
        return raw_data
        
        
    def save_meta_data(self, meta):
        """Save meta data as json file."""
        with open(self._meta_file_path, 'w') as f:
            json.dump(meta, f)

    @property
    def _dataset_size(self):
        """Size of dataset file."""
        return os.path.getsize(self._dataset_path)

    @property
    def _num_rows(self):
        """Number of rows of dataset."""
        return self._df.shape[0]

    @property
    def _columns(self):
        """Information of each column.
        For example:
        [
            {
                name: '' ,
                dtype: '' ,
                type: '', // 'category'或者'numeric'
            },
            ...
        ]
        """
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
    
    @property
    def _meta_file_name(self):
        """Get name of metadata file according to dataset name."""
        return self._dataset_name + '.meta'
    
    @property
    def _meta_file_path(self):
        """Get the file name of metadata."""
        path = os.path.join(self.dataset_root, self._meta_file_name)
        return path

    def _is_numeric(self, col_name):
        """Determine a column is numeric or category."""
        return np.issubdtype(self._df[col_name].dtype, np.number)
        
    def _get_dataset_path(self, user_id, dataset_name):
        """Check whether dataset file exists.
        If exist, return path, else return None.
        """
        dataset_name = secure_filename(dataset_name)
        dataset_path = os.path.join(self.dataset_root, dataset_name)

        # Check if dataset file exists.
        if os.path.exists(self.dataset_root) \
            and not os.path.exists(dataset_path):
            return None
        return dataset_path

