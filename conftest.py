# conftest.py
import pytest
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def browser():
    # Instala el chromedriver que coincide con tu Chrome
    chromedriver_autoinstaller.install()

    opts = webdriver.ChromeOptions()
    #opts.add_argument("--headless")
    opts.add_argument("--disable-gpu")
    opts.add_argument("--window-size=1280,800")

    # Arranca Chrome localmente
    service = Service()  # el chromedriver está ahora en PATH
    driver = webdriver.Chrome(service=service, options=opts)
    yield driver
    driver.quit()
