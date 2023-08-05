import pytest

import aishield as ais
# from pytest_mock import MockFixture

url = 'https://xxx.aishield'
token = '2e8b21f6f3e84a6287ed36999877abf0'

def test_client_noapi_fail():
    with pytest.raises(ValueError) as e:
        client = ais.AIShieldApi('', '')

def test_client_notoken_fail():
    with pytest.raises(ValueError) as e:
        client = ais.AIShieldApi(url, '')

def test_client_malformed_url_fail():
    with pytest.raises(ValueError) as e:
        client = ais.AIShieldApi('https:/aishield', 'my_token')

def test_client_correct_payload_pass():
    client = ais.AIShieldApi(url, token)
    assert client.request_processor.headers is not None

def test_job_running():
    client = ais.AIShieldApi(url, token)
    my_job_id = 'gAAAAABjaNkYdCWZDekmBc2Gh-yvYgWjFVIQdTFN2GoVZhMEl3YhOj__5DCBnGWSkaXOHPAGeOFN1K_3PUaKp5Nr4pQeVwF7Jg=='
    my_status = client.job_status(job_id=my_job_id)
    assert my_status == 'success'
