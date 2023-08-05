from aishield.constants import Attack
from aishield.tabular_classification.base_tc import TCVulnerabilityConfig
from aishield.utils.util import delete_keys_from_dict


class VulnConfig(TCVulnerabilityConfig):
    def __init__(self, defense_generate):
        super().__init__()
        if defense_generate:
            self.vulnerability_threshold = 0
        else:
            self.vulnerability_threshold = 1
        self.number_of_attack_queries = 200
        self.attack_type = 'blackbox'
        self.attack = Attack.EXTRACTION

    @property
    def number_of_attack_queries(self):
        return self.__number_of_attack_queries

    @number_of_attack_queries.setter
    def number_of_attack_queries(self, num_attack_queries):
        self.__number_of_attack_queries = num_attack_queries

    @property
    def attack_type(self):
        return self.__attack_type

    @attack_type.setter
    def attack_type(self, attack_type):
        self.__attack_type = attack_type

    def get_all_params(self):
        params = super(VulnConfig, self).get_all_params()
        params = delete_keys_from_dict(params, ['task_type', 'attack'])
        return params
