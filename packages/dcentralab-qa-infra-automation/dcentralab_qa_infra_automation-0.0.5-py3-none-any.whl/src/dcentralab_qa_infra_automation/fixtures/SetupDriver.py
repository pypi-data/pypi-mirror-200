import pytest
from selenium import webdriver
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver
from webdriver_manager.chrome import ChromeDriverManager

from seleniumPythonFramework_VeriSoft.infra.CustomEventListener import CustomEventListener

"""
setup and cleanup fixtures functions to init and close the driver. 
before the tests - init the driver, after the tests - close driver.

@Author: Efrat Cohen
@Date: 10.2022
"""


def before_test(request):
    pytest.logger.info("Test: " + request.node.nodeid + " is started ")

    # Init driver based on injected driver type
    if pytest.data_driven.get("browser") == "chrome":
        pytest.logger.info("chrome driver type injected, initialize chrome browser")
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif pytest.data_driven.get("browser") == "brave":
        pytest.logger.info("brave browser type injected, initialize brave browser")
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

    # If no driver type injected - chrome is the default
    else:
        pytest.logger.info("no browser type injected, initialize default chrome browser")
        driver = webdriver.Chrome(ChromeDriverManager().install())

    # Add event listener
    event_listener = CustomEventListener()
    event_firing_driver = EventFiringWebDriver(driver, event_listener)

    pytest.logger.info("driver :" + event_firing_driver.name + " had installed successfully")
    driver.maximize_window()
    pytest.logger.info("window had maximize")

    # Store driver in cls object
    request.cls.driver = driver
    pytest.driver = driver


# Use in cleanup fixture
def after_test(request):
    pytest.logger.info("close " + request.cls.driver.name + "driver")
    request.cls.driver.quit()
    pytest.logger.info("Test " + request.node.nodeid + " is Finished")
