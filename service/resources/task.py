import os
import json
from pathlib import Path
import queue
import threading

from flask_restful import Resource
from flask import request
from werkzeug.utils import secure_filename

import service.config as config
from service.resources.training_helper import start_model_search_process


task_id_counter = 0


message_queue = queue.Queue()


class Task(Resource):
    
    def post(self, task_id):
        """Update the status of task.
        """
        data = request.get_json()
        print(data)
        user_id = data['user_id']
        command = data['command']

        if command == 'start_training':
            dir_path = f'data/{user_id}/tasks/{task_id}'
            with open(f'{dir_path}/task_config', 'r', encoding='utf8') as f:
                config = json.load(f)
            generations = int(config['trial_times_limit'])
            t = threading.Thread(target=start_model_search_process, 
                    args=(user_id, task_id, message_queue, generations))
            t.start()
            print('Training thread start....')
        elif command == 'pending':
            pass
        elif command == 'stop_training':
            pass
        return {'message': 'success'}, 200
    
    def get(self, task_id):
        """Get training result of task.
        """
        messages = []
        while not message_queue.empty():
            messages.append(message_queue.get())
        return {'message': messages}, 200

    def put(self, task_id=None):
        """Upload a meta learning task.
        """
        data = request.get_json()
        user_id = data['user_id']
        dataset_name = data['dataset_name']
        task_type = data['task_type']
        target_col = data['target_col']
        time_limit = data['time_limit']
        trial_times_limit = data['trial_times_limit']
        data['dataset_path'] = f'data/{user_id}/dataset/{dataset_name}'

        if task_id is None:
            global task_id_counter
            task_id = f'task{task_id_counter}'
            task_id_counter += 1

        dir_path = f'data/{user_id}/tasks/{task_id}'
        Path(dir_path).mkdir(parents=True, exist_ok=True)

        data['use_time'] = 0
        data['num_trials'] = 0

        with open(f'{dir_path}/task_config', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=4)

        return {'task_id': task_id}, 200

