from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pytest

"""
init chrome driver, using ChromeDriverManager for chromeDriver installation

@Author: Efrat Cohen
@Date: 11.2022
"""


def initChromeDriver():
    """
    init chrome driver, using ChromeDriverManager for chromeDriver installation
    :return: driver - driver instance
    """
    pytest.logger.info("chrome driver type injected, initialize chrome browser")
    driver = webdriver.Chrome(ChromeDriverManager().install())
    return driver
