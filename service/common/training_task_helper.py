import os
import json

import service.config as config


class TrainingTaskHelper(object):
    
    def __init__(self, user_id, task_name):
        self._user_id = user_id
        self._task_name = task_name
    
    def save_config_file(self, config_data):
        # Create folder if not exist.
        if not os.path.exists(self._task_folder):
            os.makedirs(self._task_folder, exist_ok=True)
        with open(self._training_config_path, 'w') as f:
            json.dump(config_data, f)
    
    @property
    def _task_folder(self):
        return os.path.join(config.DATA_FOLDER,
                            self._user_id,
                            'tasks',
                            self._task_name)
    
    @property
    def _training_config_path(self):
        return os.path.join(self._task_folder,
                            config.TRAINING_CONFIG_FILE_NAME)
    
    