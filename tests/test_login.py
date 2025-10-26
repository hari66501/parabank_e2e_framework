import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.login import LoginPage
from typing import Dict  # For type hinting

from utils.logger import logger


@pytest.mark.usefixtures("browsersetup")
class TestLogin:
    driver: WebDriver
    config: dict

    @pytest.fixture(autouse=True)
    def setup_page(self, config):
        self.config = config
        self.login_page = LoginPage(self.driver)

    # Normal login using config
    # def test_enter_credentials(self):
    #     username = self.config["username"]
    #     password = self.config["password"]
    #     self.login_page.enter_username(username)
    #     self.login_page.enter_password(password)
    #     self.login_page.click_login()

    # # JSON-driven test
    # def test_login_json(self, json_data):
    #     for cred in json_data:  # IDE knows this is a dict
    #         self.login_page.enter_username(cred["username"])
    #         self.login_page.enter_password(cred["password"])
    #         self.login_page.click_login()




    # CSV-driven test
    def test_login_csv(self, csv_data):
        for cred in csv_data:
            logger.info(f"Trying login with username: {cred['username']}")
            self.login_page.enter_username(cred["username"])
            self.login_page.enter_password(cred["password"])
            self.login_page.click_login()
            logger.info(f"Login attempted for {cred['username']}")