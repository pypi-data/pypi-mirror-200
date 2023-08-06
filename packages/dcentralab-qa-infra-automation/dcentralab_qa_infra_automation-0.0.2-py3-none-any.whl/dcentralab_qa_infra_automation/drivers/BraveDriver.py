import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

"""
init brave browser driver

@Author: Efrat Cohen
@Date: 12.2022
"""


def initBraveDriver():
    """
    init brave driver, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    option = webdriver.ChromeOptions()

    # On macOS - use mac brave path
    if pytest.data_driven.get("OS") == "windows":
        option.binary_location = pytest.properties.get("brave.windows.path")
    # On windowsOS - use windows brave path
    elif pytest.data_driven.get("OS") == "mac":
        option.binary_location = pytest.properties.get("brave.mac.path")
    # If no OS injected
    else:
        pytest.logger.info("no OS type injected, brave did not add to chrome.")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    return driver
