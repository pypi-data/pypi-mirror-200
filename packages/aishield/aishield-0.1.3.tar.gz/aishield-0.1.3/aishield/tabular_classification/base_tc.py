from aishield.constants import Task, SupportedFramework
from aishield.utils.util import get_class_attributes


class TCVulnerabilityConfig:
    """
    Instatiates the base class for vulnerability config of Tabular Classification

    Returns
    -------
    Initialized config parameters required for vulnerability analysis 
    """

    def __init__(self):
        """
        Initializes the vulnerability config parameters for Tabular Classification task
        Parameters
        ----------
        defense_generate: if defense needs to be generated if vulnerabilities found in the model
        """
        self.input_dimensions = None
        self.number_of_classes = None
        self.normalize_data = "yes"
        self.model_framework = "scikit-learn"
        self.encryption_strategy = 0
        self.defense_bestonly = "no"
        self.use_model_api = 'no'
        self.model_api_details = ''
        self.is_category_columns = 'no'
        self.categorical_columns_info = []
        self.task_type = Task.TABULAR_CLASSIFICATION

    def get_all_params(self):
        """
        Get the initialized configs for vulnerability analysis
        Returns
        -------
        class_attribs: initialized configs
        """
        class_attribs = get_class_attributes(self)
        return class_attribs

    @property
    def input_dimensions(self):
        return self.__input_dimensions

    @input_dimensions.setter
    def input_dimensions(self, input_dimensions):
        if input_dimensions:
            num_data_points, num_features = input_dimensions[0], input_dimensions[1]
            valid_dim = num_data_points > 0 and num_features > 0
            if not valid_dim:
                raise Exception('number of data_points or or number of feature must be at least 1')
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

    @property
    def encryption_strategy(self):
        return self.__encryption_strategy

    @encryption_strategy.setter
    def encryption_strategy(self, encryption_strategy):
        valid_encryption_strategy = [0, 1]
        if encryption_strategy not in valid_encryption_strategy:
            raise Exception('encryption_strategy can be 0 or 1')
        self.__encryption_strategy = encryption_strategy

    @property
    def is_category_columns(self):
        return self.__is_category_columns

    @is_category_columns.setter
    def is_category_columns(self, is_category_columns):
        self.__is_category_columns = is_category_columns

    @property
    def categorical_columns_info(self):
        return self.__categorical_columns_info

    @categorical_columns_info.setter
    def categorical_columns_info(self, categorical_columns_list):
        categorical_columns_info = ','.join(categorical_columns_list)
        self.__categorical_columns_info = categorical_columns_info

    @property
    def defense_bestonly(self):
        return self.__defense_bestonly

    @defense_bestonly.setter
    def defense_bestonly(self, defense_bestonly):
        self.__defense_bestonly = defense_bestonly
