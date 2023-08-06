from auto_metamask import setupWebdriver, setupMetamask, addNetwork, changeNetwork, importPK, connectWallet, \
    downloadMetamask
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import pytest

"""
setup_with_metamask fixture function to connect wallet. 
download metamask extension to computer and connect wallet, 
open tokensfarm in the same browser that connected the wallet

@Author: Efrat Cohen
@Date: 10.2022
"""


def before_test(request):
    """
    install metamask extension, open chrome with metamask, connect the wallet.
    open tokensfarm site in this connected wallet chrome, init the driver
    :param request: the requesting test context
    """
    # Download metamask extension
    metamask_path = downloadMetamask(pytest.properties.get("download.metamask.url"))

    # Init driver with Chrome extension
    driver = setupWebdriver(metamask_path)

    # Test account
    setupMetamask(pytest.properties.get("metamask.setup"), 'testtest')
    addNetwork(pytest.properties.get("network.type"), pytest.properties.get("BSC.network.url"),
               '56', 'BNB')
    changeNetwork(pytest.properties.get("network.type"))

    # Test account
    pk = pytest.properties.get("wallet.PK")
    importPK(pk)

    driver.switch_to.new_window()

    # Go to metamask extension path
    metamask_extension_path = pytest.properties.get("metamask.extension.url")
    driver.get(metamask_extension_path)

    # Click on connect - to connect wallet
    wait = WebDriverWait(driver, 20, 1)
    wait.until(EC.element_to_be_clickable(
        (By.XPATH, '//button[text()="Connect"]'))).click()

    # Connect the wallet process, check the account
    connectWallet()

    # Navigate to site URL in current chrome with the metamask extension
    driver.get(pytest.properties.get("site.prod.url"))
    request.cls.driver = driver
