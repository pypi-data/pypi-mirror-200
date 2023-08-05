import os
from urllib.parse import urlparse
from inspect import getmembers
from types import FunctionType

from aishield.utils import logger
from aishield.utils.exceptions import AIShieldException

LOG = logger.getLogger(__name__)

def check_valid_filepath(filepath: str) -> bool:
    """
        Check if a file exists and is readable
        Parameters
        ----------
        filepath: location of the file

        Returns
        -------
        valid: True if a file exists in the specified path and is readable; otherwise False
    """

    valid = False
    if os.path.isfile(filepath) and os.access(filepath, os.R_OK):
        valid = True
    return valid


def check_or_create_directory(dir_path: str) -> None:
    """
    create directory if not present

    Parameters
    ----------
    dir_path : full path of directory

    Returns
    -------
    None. Log and Raise exception if unable to create the directory.
    """
    try:
        if os.path.isdir(dir_path):
            LOG.info("directory {} already exist".format(dir_path))
        else:
            os.mkdir(path=dir_path)
            LOG.info("directory {} created successfully".format(dir_path))
    except Exception as e:
        LOG.error("Not able to create directory at {}. Please check if correct path is provided".format(dir_path))
        raise AIShieldException(e)


def get_all_keys_by_val(dictionary: dict, value) -> list:
    """
    Get all keys of a dictionary by its value
    Parameters
    ----------
    dictionary: dictionary object
    value: value to be compared with the values of dictionary

    Returns
    -------
    found_keys: keys that matches the provided value
    """
    found_keys = []
    for key, val in dictionary.items():
        if val == value:
            found_keys.append(key)
    return found_keys


def delete_keys_from_dict(dict_obj: dict, keys_to_remove: list) -> dict:
    """
    Delete keys from a dictionary
    Parameters
    ----------
    dict_obj: dictionary object
    keys_to_remove: list of keys to be removed from the dict object

    Returns
    -------
    dict_obj_cpy: modified dictionary with the keys removed
    """
    dict_obj_cpy = dict_obj.copy()
    for k in keys_to_remove:
        dict_obj_cpy.pop(k, None)  # pop operation eliminates the need for key existence testing
    return dict_obj_cpy


def get_class_attributes(class_obj):
    """
    Gets the attributes of a class
    Parameters
    ----------
    class_obj: object of a class

    Returns
    -------
    The attributes of a class from the instantiated class object
    """
    disallowed_names = {
        name for name, value in getmembers(type(class_obj))
        if isinstance(value, FunctionType)}
    return {
        name: getattr(class_obj, name) for name in dir(class_obj)
        if name[0] != '_' and name not in disallowed_names and hasattr(class_obj, name)}


def uri_validator(url) -> bool:
    """
    check if the uri is valid
    Parameters
    ----------
    url: uri

    Returns
    -------
    valid: True or False
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
