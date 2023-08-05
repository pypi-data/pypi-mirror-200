from pprint import pprint

from aishield.constants import Task, SupportedFramework
from aishield.utils.util import get_class_attributes


class ICVulnerabilityConfig:
    """
    Instantiates the base class for vulnerability config of Image Classification

    Returns
    -------
    Initialized config parameters required for vulnerability analysis 
    """

    def __init__(self):
        """
        Initializes the vulnerability config parameters for Image Classification task
        Parameters
        ----------
        defense_generate: if defense needs to be generated if vulnerabilities found in the model
        """
        self.input_dimensions = None
        self.number_of_classes = None
        self.normalize_data = "yes"
        self.model_framework = "tensorflow"
        self.task_type = Task.IMAGE_CLASSIFICATION

    def get_all_params(self):
        """
        Get the initialized configs for vulnerability analysis
        Returns
        -------
        class_attribs: initialized configs
        """
        class_attribs = get_class_attributes(self)
        # pprint(class_attribs)
        return class_attribs

    @property
    def input_dimensions(self):
        return self.__input_dimensions

    @input_dimensions.setter
    def input_dimensions(self, input_dimensions):
        if input_dimensions:
            height, width, channel = input_dimensions[0], input_dimensions[1], input_dimensions[2]
            valid_channel_val = channel == 1 or channel == 3
            if not valid_channel_val:
                raise Exception('channel must be 1(greyscale) or 3(color)')
            input_dimensions = str(input_dimensions)
        self.__input_dimensions = input_dimensions

    @property
    def number_of_classes(self):
        return self.__number_of_classes

    @number_of_classes.setter
    def number_of_classes(self, num_classes):
        if num_classes and num_classes == 0:
            raise Exception('Number of classes must be >=1')
        self.__number_of_classes = num_classes

    @property
    def normalize_data(self):
        return self.__normalize_data

    @normalize_data.setter
    def normalize_data(self, normalize_data):
        if normalize_data.lower() not in ['yes', 'no']:
            raise Exception('normalize_data field can be yes or no')
        self.__normalize_data = normalize_data

    @property
    def model_framework(self):
        return self.__model_framework

    @model_framework.setter
    def model_framework(self, model_framework):
        if model_framework.lower() not in SupportedFramework.valid_types():
            raise Exception('model_framework provided {} not supported. Supported: {}'
                            .format(model_framework, ', '.join(SupportedFramework.valid_types())))
        self.__model_framework = model_framework

