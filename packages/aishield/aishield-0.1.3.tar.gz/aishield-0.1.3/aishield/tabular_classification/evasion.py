from aishield.constants import Attack
from aishield.tabular_classification.base_tc import TCVulnerabilityConfig
from aishield.utils.util import delete_keys_from_dict


class VulnConfig(TCVulnerabilityConfig):
    def __init__(self, defense_generate):
        super().__init__()
        self.attack = Attack.EVASION

    def get_all_params(self):
        params = super(VulnConfig, self).get_all_params()
        params = delete_keys_from_dict(params, ['task_type', 'attack', 'vulnerability_threshold'])
        return params
