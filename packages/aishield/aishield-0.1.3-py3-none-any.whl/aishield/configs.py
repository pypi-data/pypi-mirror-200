import os
from aishield.constants import (
    FileFormat,
    ReportType,
)
from aishield.utils.util import check_or_create_directory


class JobDetails:
    """
    Instantiates to details of a vulnerability analysis job
    """
    def __init__(self, job_id=None, job_monitor_uri=None, model_id=None, data_upload_uri=None, label_upload_uri=None,
                 minmax_upload_uri: str = None, model_upload_uri=None, clean_model_upload_uris=[]):
        """
        Constructor for Job Details class.
        Parameters
        ----------
        job_id: job_id of the submitted job
        job_monitor_uri: uri for monitoring the progress of job
        model_id: model id obtained after model registration
        data_upload_uri: uri returned by model registration service where data file in zip needs to be uploaded
        label_upload_uri: uri returned by model registration service where label file in zip needs to be uploaded
        minmax_upload_uri: uri returned by model registration service where minmax(for tabular data) file in zip needs to be uploaded
        model_upload_uri: uri returned by model registration service where model file in zip needs to be uploaded
        clean_model_upload_uris: uri's returned by model registration service where clean model files in zip needs to be uploaded (for model poison check)
        """
        self.job_id = job_id
        self.job_monitor_uri = job_monitor_uri
        self.model_id = model_id
        self.data_upload_uri = data_upload_uri
        self.label_upload_uri = label_upload_uri
        self.model_upload_uri = model_upload_uri
        self.minmax_upload_uri = minmax_upload_uri  # for Tabular datatype
        self.clean_model_upload_uris = clean_model_upload_uris  # for model poison analysis


    @property
    def job_id(self):
        return self.__job_id

    @job_id.setter
    def job_id(self, job_id):
        self.__job_id = job_id

    @property
    def job_monitor_uri(self):
        return self.__job_monitor_uri

    @job_monitor_uri.setter
    def job_monitor_uri(self, job_monitor_uri):
        self.__job_monitor_uri = job_monitor_uri

    @property
    def data_upload_uri(self):
        return self.__data_upload_uri

    @data_upload_uri.setter
    def data_upload_uri(self, data_upload_uri):
        self.__data_upload_uri = data_upload_uri

    @property
    def label_upload_uri(self):
        return self.__label_upload_uri

    @label_upload_uri.setter
    def label_upload_uri(self, label_upload_uri):
        self.__label_upload_uri = label_upload_uri

    @property
    def minmax_upload_uri(self):
        return self.__minmax_upload_uri

    @minmax_upload_uri.setter
    def minmax_upload_uri(self, minmax_upload_uri):
        self.__minmax_upload_uri = minmax_upload_uri

    @property
    def model_upload_uri(self):
        return self.__model_upload_uri

    @model_upload_uri.setter
    def model_upload_uri(self, model_upload_uri):
        self.__model_upload_uri = model_upload_uri

    @property
    def clean_model_upload_uris(self):
        return self.__clean_model_upload_uris

    @clean_model_upload_uris.setter
    def clean_model_upload_uris(self, clean_model_upload_uris):
        self.__clean_model_upload_uris = clean_model_upload_uris

    @property
    def model_id(self):
        return self.__model_id

    @model_id.setter
    def model_id(self, model_id):
        self.__model_id = model_id


class OutputConf:
    """
    OutputConf for getting reports(vulnerability/defense) or artifacts(defense model/sample attack data)
    """

    def __init__(self, report_type: ReportType = ReportType.VULNERABILITY, file_format: FileFormat = FileFormat.PDF,
                 save_folder_path=os.getcwd()):
        """
        Sets the OutputConf for getting reports(vulnerability/defense) or artifacts(defense model/sample attack data)
        Parameters
        ----------
        report_type: Report Type (Options : Vulnerability , Defense, Defense_artifact, Attack_samples)
        file_format: File format Type (Options : all, txt , pdf, json, xml}
        save_folder_path: output path where the artifacts would be saved
        """
        self.report_type = report_type
        self.file_format = file_format
        self.save_folder_path = save_folder_path

    @property
    def report_type(self):
        return self.__report_type

    @report_type.setter
    def report_type(self, report_type):
        self.__report_type = report_type

    @property
    def file_format(self):
        return self.__file_format

    @file_format.setter
    def file_format(self, file_format):
        self.__file_format = file_format

    @property
    def save_folder_path(self):
        return self.__save_folder_path

    @save_folder_path.setter
    def save_folder_path(self, save_folder_path):
        check_or_create_directory(save_folder_path)
        self.__save_folder_path = save_folder_path
