import pytest
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions

"""
open site with extension via CRX. to any browser type.

@Author: Efrat Cohen
@Date: 12.2022
"""


def before_test(request):
    """
    get crx extension file, setup driver - open the site with extension.
    store the driver to use him in different fixtures and pages.
    if brave browser injected - add the option to driver initialization
    :param request: the requesting test context
    """
    chrome_options = ChromeOptions()
    # In metamask wallet type
    if pytest.data_driven.get("wallet_type") == 'MetaMask':
        chrome_options.add_extension(pytest.user_dir + pytest.properties.get("metamask.extension.crx"))
    elif pytest.data_driven.get("wallet_type") == 'Coinbase':
        chrome_options.add_extension(pytest.user_dir + pytest.properties.get("coinbase.extension.crx"))

    # If brave browser driver type injected - add brave binary_location to chrome_options
    if pytest.data_driven.get("browser") == "brave":
        pytest.logger.info("brave browser type injected, initialize brave browser")

        # On macOS - use mac brave path
        if pytest.data_driven.get("OS") == "windows":
            chrome_options.binary_location = pytest.properties.get("brave.windows.path")
            # On windowsOS - use windows brave path
        elif pytest.data_driven.get("OS") == "mac":
            chrome_options.binary_location = pytest.properties.get("brave.mac.path")
            # If no OS injected
        else:
            pytest.logger.info("no OS type injected, brave did not add to chrome.")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.maximize_window()

    request.cls.driver = driver
