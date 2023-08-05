from aishield.constants import Attack
from aishield.image_classification.base_ic import ICVulnerabilityConfig
from aishield.utils.util import delete_keys_from_dict
from aishield.utils import logger

LOG = logger.getLogger(__name__)

class VulnConfig(ICVulnerabilityConfig):
    def __init__(self, defense_generate):
        super().__init__()
        if defense_generate:
            self.vulnerability_threshold = 0
        else:
            self.vulnerability_threshold = 1
        self.attack = Attack.POISONING


    def get_all_params(self):
        params = super(VulnConfig, self).get_all_params()
        params = delete_keys_from_dict(params, ['task_type', 'attack'])
        return params
