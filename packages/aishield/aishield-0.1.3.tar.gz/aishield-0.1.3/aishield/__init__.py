from aishield.constants import (
    Attack,
    Task,
    FileFormat,
    ReportType,
)
from aishield.aishield_api import (
    AIShieldApi,
    VulnConfig,
    OutputConf,
)


def get_type(process, process_val):
    """
    Function to get a valid process type.
    Given a process and its value, supported AIShield Enum will be returned for further processing.
    Raise Error if for any invalid value not supported
    Parameters
    ----------
    process: process type: task, analysis, report, file_format
    process_val: value of the process.
        Example: image_classification for process: task, extraction for process: analysis, etc.
                get_type("task", "image forecasting")
                get_type("analysis", "extraction")

    Returns
    -------
        The Enum value compatible for AIShield processing
    """
    process = process.lower()
    supported_process = ['task', 'analysis', 'report', 'file_format']
    try:
        if process == 'task':
            valid_types = Task.valid_types()
            val = Task(process_val)
        elif process == 'analysis':
            valid_types = Attack.valid_types()
            val = Attack(process_val)
        elif process == 'report':
            valid_types = ReportType.valid_types()
            val = ReportType(process_val)
        elif process == 'file_format':
            valid_types = FileFormat.valid_types()
            val = FileFormat(process_val)
        else:
            raise ValueError('process {} is invalid. Supported {}'.format(process, ', '.join(supported_process)))
    except ValueError:
        raise ValueError('provided {} value {} is invalid. Accepted are: {}.'.format(process, process_val, valid_types))
    return val
