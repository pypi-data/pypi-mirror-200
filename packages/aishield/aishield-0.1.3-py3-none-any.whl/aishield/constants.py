from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def valid_types(cls):
        return list(map(lambda c: c.value, cls))


class Attack(ExtendedEnum):
    EXTRACTION = 'extraction'
    EVASION = 'evasion'
    INFERENCE = 'inference'
    POISONING = 'poisoning'


class Task(ExtendedEnum):
    IMAGE_CLASSIFICATION = 'image_classification'
    IMAGE_SEGMENTATION = 'image_segmentation'
    TIMESERIES_FORECAST = 'timeseries_forecast'
    NLP = 'nlp'
    TABULAR_CLASSIFICATION = 'tabular_classification'


class ReportType(ExtendedEnum):
    VULNERABILITY = 'vulnerability'
    DEFENSE = 'defense'
    DEFENSE_ARTIFACT = 'defense_artifact'
    ATTACK_SAMPLES = 'attack_samples'


class FileFormat(ExtendedEnum):
    TXT = 'txt'
    PDF = 'pdf'
    JSON = 'json'
    XML = 'xml'
    ALL = 'all'


class SupportedFramework(ExtendedEnum):
    TENSORFLOW = 'tensorflow'
    SCIKIT_LEARN = 'scikit-learn'


class UploadURIKeys(ExtendedEnum):
    MODEL_ID_KEY = 'model_id'
    URL_FIELD_KEY = 'urls'
    DATA_UPLOAD_URI_KEY = 'data_upload_url'
    LABEL_UPLOAD_URI_KEY = 'label_upload_url'
    MODEL_UPLOAD_URI_KEY = 'model_upload_url'
    MINMAX_UPLOAD_URI_KEY = 'minmax_upload_url'
    CLEAN_MODEL1_UPLOAD_URI_KEY = 'clean_model1_upload_url'
    CLEAN_MODEL2_UPLOAD_URI_KEY = 'clean_model2_upload_url'


class ResponseStatus(ExtendedEnum):
    SUCCESS = 'success'
    FAILED = 'failed'
