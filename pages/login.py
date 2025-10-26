import allure
from selenium.webdriver.common.by import By

class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username = (By.NAME, "username")
        self.password = (By.NAME, "password")
        self.login_btn = (By.XPATH, "//button[@type='submit']")

    @allure.step("Enter username: {username}")
    def enter_username(self, username):
        self.driver.find_element(*self.username).send_keys(username)

    @allure.step("Enter password: {password}")
    def enter_password(self, password):
        self.driver.find_element(*self.password).send_keys(password)

    @allure.step("click login: {login}")
    def click_login(self):
        self.driver.find_element(*self.login_btn).click()

    def login(self, username, password):
        self.enter_username(username)
        self.enter_password(password)
        self.click_login()
