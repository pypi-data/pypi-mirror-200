from typing import Optional

from aishield.connection import RequestProcessor
from aishield.constants import (
    FileFormat,
    ReportType,
    Attack,
    Task,
    UploadURIKeys,
    ResponseStatus
)
from aishield.configs import (
    OutputConf,
    JobDetails
)
from aishield.image_classification import (
    extraction as ic_extraction,
    evasion as ic_evasion,
    poision as ic_poison
)
from aishield.tabular_classification import (
    extraction as tc_extraction,
    evasion as tc_evasion
)
from aishield.utils.util import (
    uri_validator,
    get_all_keys_by_val
)
from aishield.utils.util import delete_keys_from_dict


class VulnConfig:
    """
    Instantiates the vulnerability configs based on task and attack type
    """

    def __new__(cls, task_type: Optional[Task] = Task.IMAGE_CLASSIFICATION,
                analysis_type: Optional[Attack] = Attack.EXTRACTION,
                defense_generate: Optional[bool] = True):
        """
        Return the Vulnerability Config object

        Parameters
        ----------
        task_type: Type of task. Example: Image Classification, Image Segmentation, NLP, etc.
        analysis_type: Type of analysis_type(attack) for which vulnerability assessment has to be done.Example: Extraction, Evasion,etc.
        defense_generate: Boolean flag to specify if defense needs to be generated if model found to be vulnerable

        Returns
        -------
        vul_config_obj : Class Object
        """
        task_type_val = task_type.value
        attack_val = analysis_type.value
        if task_type_val not in Task.valid_types():
            raise ValueError('task_type param value {} is not in one of the accepted values {}.'.format(task_type_val,
                                                                                                        Task.valid_types()))
        if attack_val not in Attack.valid_types():
            raise ValueError('attack param value {} is not in one of the accepted values {}.'.format(attack_val,
                                                                                                     Attack.valid_types()))

        if task_type == Task.IMAGE_CLASSIFICATION:
            if analysis_type == Attack.EXTRACTION:
                vul_config_obj = ic_extraction.VulnConfig(defense_generate)
            elif analysis_type == Attack.EVASION:
                vul_config_obj = ic_evasion.VulnConfig(defense_generate)
            elif analysis_type == Attack.POISONING:
                vul_config_obj = ic_poison.VulnConfig(defense_generate)
            else:
                raise NotImplementedError('Feature coming soon')
        elif task_type == Task.TABULAR_CLASSIFICATION:
            if analysis_type == Attack.EXTRACTION:
                vul_config_obj = tc_extraction.VulnConfig(defense_generate)
            elif analysis_type == Attack.EVASION:
                vul_config_obj = tc_evasion.VulnConfig(defense_generate)
            else:
                raise NotImplementedError('Feature coming soon')
        elif task_type == Task.TIMESERIES_FORECAST:
            raise NotImplementedError('Feature coming soon')
        elif task_type == Task.NLP:
            raise NotImplementedError('Feature coming soon')
        elif task_type == Task.IMAGE_SEGMENTATION:
            raise NotImplementedError('Feature coming soon')
        else:
            raise NotImplementedError('New task-pairs would be added soon')
        return vul_config_obj


class AIShieldApi:
    """
    Instantiates for performing vulnerability analysis
    """

    def __init__(self, api_url: str, api_key: str, org_id: str):
        """
        Initializes the AIShield API with request headers

        Parameters
        ----------
        api_url: api endpoint of AIShield vulnerability analysis
        api_key: user api key
        org_id: organization key
        """
        if not api_url:
            raise ValueError('AIShield api is not provided')
        if not api_key:
            raise ValueError('api_key is not provided')
        if not org_id:
            raise ValueError('org_id is not provided')
        if not uri_validator(api_url):
            raise ValueError('aishield api is invalid')

        headers = {
            'Cache-Control': 'no-cache',
            'x-api-key': api_key,
            'Org-Id': org_id
        }
        self.request_processor = RequestProcessor(api_url, headers)
        self.job_details = JobDetails()
        self.task_type = None
        self.analysis_type = None
        self.job_payload = None

    def register_model(self, task_type: Optional[Task] = Task.IMAGE_CLASSIFICATION,
                       analysis_type: Optional[Attack] = Attack.EXTRACTION):
        """
            Perform the initial model registration process for vulnerability analysis

            Parameters
            ----------
            task_type: Type of task. Example: Image Classification, Image Segmentation, NLP, etc.
            analysis_type: Type of analysis_type(attack) for which vulnerability assessment has to be done.Example: Extraction, Evasion,etc.

            Returns
            -------
            status: registration status: success or failed
            job_details: having information of model_id, data_upload_uri, label_upload_uri, model_upload_uri
        """
        self.task_type = task_type
        self.analysis_type = analysis_type
        model_registration_payload = {
            'task_type': task_type.value,
            "analysis_type": analysis_type.value
        }
        status, response_json = self.request_processor.register(payload=model_registration_payload)
        response_json_urls = response_json[UploadURIKeys.URL_FIELD_KEY.value]
        self.job_details.model_id = response_json[UploadURIKeys.MODEL_ID_KEY.value]
        self.job_details.data_upload_uri = response_json_urls[UploadURIKeys.DATA_UPLOAD_URI_KEY.value]
        self.job_details.model_upload_uri = response_json_urls[UploadURIKeys.MODEL_UPLOAD_URI_KEY.value]
        if task_type == Task.IMAGE_CLASSIFICATION:
            self.job_details.label_upload_uri = response_json_urls[UploadURIKeys.LABEL_UPLOAD_URI_KEY.value]
            if analysis_type == Attack.POISONING:
                clean_model_upload_uris = [response_json_urls[UploadURIKeys.CLEAN_MODEL1_UPLOAD_URI_KEY.value],
                                           response_json_urls[UploadURIKeys.CLEAN_MODEL2_UPLOAD_URI_KEY.value]]
                self.job_details.clean_model_upload_uris = clean_model_upload_uris
        elif task_type == Task.TABULAR_CLASSIFICATION:
            self.job_details.minmax_upload_uri = response_json_urls[UploadURIKeys.MINMAX_UPLOAD_URI_KEY.value]
        else:
            raise NotImplementedError('New task-pairs would be added soon')
        return status, self.job_details

    def upload_input_artifacts(self, job_details: JobDetails, data_path: str = None, label_path: str = None,
                               minmax_path: str = None, model_path: str = None, clean_model_paths: list = None) -> list:
        """
            Upload the input artifacts such as data, label and model file

            Parameters
            ----------
            job_details: object having information such as model_id, data_upload_uri, label_upload_uri, model_upload_uri
            data_path: location of data file
            label_path: location of label file
            minmax_path: location of minmax file(used for tabular data)
            model_path: location of model file
            clean_model_paths: location of clean model files. Required for model poisoning check

            Returns
            -------
            upload_status_msg: all upload messages in a list
        """
        if clean_model_paths is None:
            clean_model_paths = []
        upload_status_msg = []
        error_flag = False
        if data_path:
            data_upload_uri = job_details.data_upload_uri
            upload_status = self.request_processor.upload_file(file_path=data_path, upload_uri=data_upload_uri)
            if upload_status == ResponseStatus.SUCCESS:
                upload_status_msg.append('data file upload successful')
            else:
                error_flag = True
                upload_status_msg.append('data file upload failed')
        if label_path:
            label_upload_uri = job_details.label_upload_uri
            upload_status = self.request_processor.upload_file(file_path=label_path, upload_uri=label_upload_uri)
            if upload_status == ResponseStatus.SUCCESS:
                upload_status_msg.append('label file upload successful')
            else:
                error_flag = True
                upload_status_msg.append('label file upload failed')

        if minmax_path:
            minmax_upload_uri = job_details.minmax_upload_uri
            upload_status = self.request_processor.upload_file(file_path=minmax_path, upload_uri=minmax_upload_uri)
            if upload_status == ResponseStatus.SUCCESS:
                upload_status_msg.append('minmax file upload successful')
            else:
                error_flag = True
                upload_status_msg.append('minmax file upload failed')

        if model_path:
            model_upload_uri = job_details.model_upload_uri
            upload_status = self.request_processor.upload_file(file_path=model_path, upload_uri=model_upload_uri)
            if upload_status == ResponseStatus.SUCCESS:
                upload_status_msg.append('model file upload successful')
            else:
                error_flag = True
                upload_status_msg.append('model file upload failed')

        if clean_model_paths:
            num_clean_models_required = 2
            if len(clean_model_paths) < 2 or not all(clean_model_paths):
                raise Exception('Model poison analysis requires atleast {} numbers of clean model'.format(num_clean_models_required))
            clean_model_upload_uris = job_details.clean_model_upload_uris
            for idx in range(num_clean_models_required):
                upload_status = self.request_processor.upload_file(file_path=clean_model_paths[idx], upload_uri=clean_model_upload_uris[idx])
                if upload_status == ResponseStatus.SUCCESS:
                    upload_status_msg.append('clean model file{} upload successful'.format(idx))
                else:
                    error_flag = True
                    upload_status_msg.append('clean model file{} upload failed'.format(idx))
        if error_flag:
            raise Exception('some error occurred while uploading. Status is: {}'.format(', '.join(upload_status_msg)))
        return upload_status_msg

    def vuln_analysis(self, model_id: str = None, vuln_config: VulnConfig = None):
        """
        Perform Vulnerability analysis of the model

        Parameters
        ----------
        model_id: model id obtained after model registration
        vuln_config: configs for vulnerability analysis of VulnConfig type

        Returns
        -------
        status: job status: success or failed
        job_details: having information such as job_id, monitoring link
        """

        if not model_id:
            raise ValueError('model_id must be provided')
        if not vuln_config:
            raise ValueError('vulnerability config must be provided')

        payload = {key: getattr(vuln_config, key) for key in dir(vuln_config) if not key.startswith('_')}
        payload = delete_keys_from_dict(payload, ['task_type', 'attack', 'get_all_params'])  # delete non-relevant params for API call
        # validation - raise error any key in payload has None value
        keys_with_none_val = get_all_keys_by_val(payload, None)
        if keys_with_none_val:
            raise ValueError('None values found for {}.'.format(', '.join(keys_with_none_val)))

        task_type = vuln_config.task_type
        attack_strategy = vuln_config.attack

        if self.task_type != task_type or attack_strategy != self.analysis_type:
            raise Exception('Mismatch in task_type, analysis_type specified in model registration and analysis')

        self.job_payload = payload
        status, response_json = self.request_processor.send_for_analysis(model_id=model_id, payload=payload)
        self.job_details.job_id = response_json['job_id']
        self.job_details.job_monitor_uri = response_json['monitor_link']
        return status, self.job_details

    def job_status(self, job_id):
        """
        Prints the status of each vulnerability analysis while the job is running.
        Once job completes, returns with status: success or failed

        Parameters
        ----------
        job_id: job_id returned from the request

        Returns
        -------
        status: success or failed
        """
        status = self.request_processor.get_job_status(job_id=job_id, analysis_type=self.analysis_type,
                                                       job_payload=self.job_payload)
        return status

    def save_job_report(self, job_id: str = None, output_config: OutputConf = None) -> str:
        """
        Save the artifacts of the vulnerability analysis.

        Parameters
        ----------
        job_id: job_id returned from the request
        output_config: object with OutputConf Type

        Returns
        -------
        saved_loc: location where the artifact got saved.
        """
        if not job_id or job_id is None:
            raise ValueError('invalid job id value')
        file_format = output_config.file_format.value.lower()
        report_type = output_config.report_type.value.lower()
        save_folder_path = output_config.save_folder_path

        if file_format not in FileFormat.valid_types():
            raise ValueError('invalid file_format value {}. Must be one of {}'.format(file_format,
                                                                                      FileFormat.valid_types()))
        if report_type not in ReportType.valid_types():
            raise ValueError('invalid report_type value {}. Must be one of {}'.format(report_type,
                                                                                ReportType.valid_types()))

        # poisoning supports only pdf report format type
        if self.analysis_type == Attack.POISONING and not (FileFormat(output_config.file_format) == FileFormat.PDF):
            raise ValueError('invalid file_format value. poisoning analysis supports only pdf type')

        saved_loc = self.request_processor.get_artifacts(job_id=job_id, report_type=report_type,
                                                         file_format=file_format,
                                                         save_folder_path=save_folder_path)
        return saved_loc
