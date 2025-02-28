import os
import pytest

from kount import config


def pytest_addoption(parser):
    parser.addoption('--conf-key', action='store',
                     default=os.environ.get('CONF_KEY', ''))
    parser.addoption('--api-key', action='store',
                     default=os.environ.get('RIS_SDK_SANDBOX_API_KEY', ''))
    parser.addoption('--merchant-id', action='store', 
                     default=os.environ.get('RIS_SDK_SANDBOX_MERCHANT_ID', ''))
    parser.addoption('--api-url', action='store', 
                     default=os.environ.get('RIS_SDK_SANDBOX_URL', 'https://risk.test.kount.net'))
    parser.addoption('--migration-mode-enabled', action='store',
                     default=os.environ.get('MIGRATION_MODE_ENABLED', 'false'))
    parser.addoption('--pf-client-id', action='store',
                     default=os.environ.get('PF_CLIENT_ID', None))
    parser.addoption('--pf-auth-endpoint', action='store',
                     default=os.environ.get('PF_AUTH_ENDPOINT', 'https://login.kount.com/oauth2/ausdppkujzCPQuIrY357/v1/token'))
    parser.addoption('--pf-api-endpoint', action='store',
                     default=os.environ.get('PF_API_ENDPOINT', 'https://api-sandbox.kount.com/commerce/ris'))
    parser.addoption('--pf-api-key', action='store',
                     default=os.environ.get('PF_API_KEY', 'API_KEY_GOES_HERE'))


@pytest.fixture(scope='session', autouse=True)
def conf_key(request):
    try:
        config.SDKConfig.setup(request.config.getoption('--conf-key'))
    except ValueError as e:
        if not config.SDKConfig.get_configuration_key():
            msg = "Configuration key not set, use --conf-key or " \
                  "set environment variable CONF_KEY"
        else:
            msg = 'Configuration key error: %s' % str(e)
        pytest.exit(msg)


@pytest.fixture(scope='class')
def api_key(request):
    request.cls.api_key = request.config.getoption('--api-key')


@pytest.fixture(scope='class')
def merchant_id(request):
    request.cls.merchant_id = request.config.getoption('--merchant-id')


@pytest.fixture(scope='class')
def api_url(request):
    request.cls.api_url = request.config.getoption('--api-url')


@pytest.fixture(scope='class')
def pf_client_id(request):
    request.cls.pf_client_id = request.config.getoption('--pf-client-id')


@pytest.fixture(scope='class')
def pf_auth_endpoint(request):
    request.cls.pf_auth_endpoint = request.config.getoption('--pf-auth-endpoint')


@pytest.fixture(scope='class')
def pf_api_endpoint(request):
    request.cls.pf_api_endpoint = request.config.getoption('--pf-api-endpoint')


@pytest.fixture(scope='class')
def pf_api_key(request):
    request.cls.pf_api_key = request.config.getoption('--pf-api-key')


@pytest.fixture(scope='class')
def migration_mode_enabled(request):
    request.cls.migration_mode_enabled = request.config.getoption('--migration-mode-enabled')
    if request.cls.migration_mode_enabled.lower() == 'true':
        request.cls.migration_mode_enabled = True
    else:
        request.cls.migration_mode_enabled = False