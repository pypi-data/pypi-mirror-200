from aishield.constants import Attack
from aishield.image_classification.base_ic import ICVulnerabilityConfig
from aishield.utils.util import delete_keys_from_dict


class VulnConfig(ICVulnerabilityConfig):
    def __init__(self, defense_generate):
        super().__init__()
        if defense_generate:
            self.vulnerability_threshold = 0
        else:
            self.vulnerability_threshold = 1
        self.number_of_attack_queries = 200
        self.attack_type = 'blackbox'
        self.encryption_strategy = 0
        self.use_model_api = 'no'
        self.model_api_details = ''
        self.defense_bestonly = "no"
        self.attack = Attack.EXTRACTION

    @property
    def number_of_attack_queries(self):
        return self.__number_of_attack_queries

    @number_of_attack_queries.setter
    def number_of_attack_queries(self, num_attack_queries):
        self.__number_of_attack_queries = num_attack_queries

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
    def attack_type(self):
        return self.__attack_type

    @attack_type.setter
    def attack_type(self, attack_type):
        self.__attack_type = attack_type

    @property
    def defense_bestonly(self):
        return self.__defense_bestonly

    @defense_bestonly.setter
    def defense_bestonly(self, defense_bestonly):
        self.__defense_bestonly = defense_bestonly

    def get_all_params(self):
        params = super(VulnConfig, self).get_all_params()
        params = delete_keys_from_dict(params, ['task_type', 'attack'])
        return params
