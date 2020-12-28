import json

from sklearn.model_selection import train_test_split
from sklearn.utils import Bunch
import numpy as np
import pandas as pd

from service.lib.tpot import TPOTRegressor


def load_dataset(filename, target_col):
    df = pd.read_csv(filename)
    target = df[target_col].to_numpy()
    df = df.drop(target_col, 1)
    data = df.to_numpy()
    return Bunch(data=data, target=target)


def search_regression_model(whole_data, queue, generations):
    X_train, X_test, y_train, y_test = train_test_split(whole_data.data, whole_data.target,
                                                        train_size=0.75, test_size=0.25, random_state=42)
    tpot = TPOTRegressor(generations=generations, population_size=30, verbosity=2, random_state=42)
    print('begin fit model....')
    tpot.fit(X_train, y_train, queue)
    print(tpot.score(X_test, y_test))
    tpot.export('tpot_boston_pipeline.py')


def start_model_search_process(user_id, task_id, queue, generations):
    path = f'data/{user_id}/tasks/{task_id}/task_config'
    with open(path, 'r', encoding='utf8') as f:
        config_data = json.load(f)
        dataset_path = config_data['dataset_path']
        target_col = config_data['target_col']
        task_type = config_data['task_type']
        if task_type == 'regression':
            dataset = load_dataset(dataset_path, target_col)
            search_regression_model(dataset, queue, generations)
