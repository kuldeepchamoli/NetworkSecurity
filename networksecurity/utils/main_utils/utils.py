import yaml
import os, sys
import pickle
# import dill  # Uncomment if needed

import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "r") as yaml_file:  # ✅ Use "r" not "rb" for text files
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def save_numpy_array_data(file_path: str, array: np.ndarray) -> None:
    """
    Save numpy array to file
    file_path: str - location to save the array
    array: np.ndarray - data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.ndarray:
    """
    Load numpy array from data file
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered the save_object method of MainUtils class")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of MainUtils class")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"The file: {file_path} does not exist")

        # Check file extension
        _, ext = os.path.splitext(file_path)

        with open(file_path, "rb") as file_obj:
            if ext == ".pkl":
                return pickle.load(file_obj)
            elif ext == ".npy":
                return np.load(file_obj)  # For numpy arrays
            else:
                raise ValueError(f"Unsupported file extension '{ext}' for file: {file_path}")
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e


def evaluate_model(X_train, y_train, X_test, y_test, models: dict, param: dict) -> dict:
    """
    Evaluate models using GridSearchCV and return a dictionary of model scores
    """
    try:
        report = {}

        for model_name, model in models.items():
            parameters = param.get(model_name, {})

            if parameters:
                gs = GridSearchCV(model, parameters, cv=3, n_jobs=-1)
                gs.fit(X_train, y_train)
                model.set_params(**gs.best_params_)

            model.fit(X_train, y_train)

            y_train_pred = model.predict(X_train)
            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
