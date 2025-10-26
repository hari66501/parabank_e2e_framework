from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

class BrowserFactory:

    @staticmethod
    def get_driver(browser_name: str = "chrome", headless: bool = False, implicit_wait: int = 10):
        browser_name = browser_name.lower()

        if browser_name == "chrome":
            options = ChromeOptions()
            if headless:
                options.add_argument("--headless=new")  # Recommended for latest Chrome
            options.add_argument("--start-maximized")
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

        elif browser_name == "firefox":
            options = FirefoxOptions()
            if headless:
                options.headless = True
            driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
            driver.maximize_window()  # Firefox doesn't auto-maximize

        elif browser_name == "edge":
            options = EdgeOptions()
            if headless:
                options.add_argument("--headless=new")
            options.add_argument("--start-maximized")
            driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)

        else:
            raise ValueError(f"Browser '{browser_name}' is not supported. Use chrome, firefox, or edge.")

        # Global implicit wait
        driver.implicitly_wait(implicit_wait)
        return driver
