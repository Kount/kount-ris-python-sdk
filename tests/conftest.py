import os
import pytest

from kount import config
from kount.settings import TEST_API_KEY, TEST_API_URL, TEST_MERCHANT_ID

TEST_API_URL = TEST_API_URL

TEST_API_KEY = TEST_API_KEY

TEST_MERCHANT = TEST_MERCHANT_ID


def pytest_addoption(parser):
    parser.addoption('--conf-key', action='store',
                     default=os.environ.get('CONF_KEY', ''))
    parser.addoption('--api-key', action='store', default=TEST_API_KEY)
    parser.addoption('--merchant-id', action='store', default=TEST_MERCHANT)
    parser.addoption('--api-url', action='store', default=TEST_API_URL)


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

