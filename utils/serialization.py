import pickle

from utils.logger import logger


def save_pickle(obj, filepath):
    """
    Save any Python object to disk using pickle.
    """
    with open(filepath, "wb") as file:
        pickle.dump(obj, file)

    logger.info(f"Saved pickle to {filepath}")


def load_pickle(filepath):
    """
    Load a pickled Python object.
    """
    with open(filepath, "rb") as file:
        obj = pickle.load(file)

    logger.info(f"Loaded pickle from {filepath}")

    return obj