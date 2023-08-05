from aishield.constants import Attack
from aishield.image_classification.base_ic import ICVulnerabilityConfig
from aishield.utils.util import delete_keys_from_dict


class VulnConfig(ICVulnerabilityConfig):
    def __init__(self, defense_generate):
        super().__init__()
        self.encryption_strategy = 0
        self.use_model_api = 'no'
        self.model_api_details = ''
        self.defense_bestonly = "no"
        self.attack = Attack.EVASION

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
    def defense_bestonly(self):
        return self.__defense_bestonly

    @defense_bestonly.setter
    def defense_bestonly(self, defense_bestonly):
        self.__defense_bestonly = defense_bestonly

    def get_all_params(self):
        params = super(VulnConfig, self).get_all_params()
        params = delete_keys_from_dict(params, ['task_type', 'attack'])
        return params
