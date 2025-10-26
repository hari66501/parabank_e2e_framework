import pytest
import sys
import os
from datetime import datetime
import logging

# Optional Allure
try:
    import allure
except ImportError:
    allure = None

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.excel_utils import read_excel
from utils.csv_utils import read_csv
from utils.json_utils import read_json
from utils.read_config import ReadConfig
from core.driverfactory import BrowserFactory

# -------------------- Logging Setup --------------------
logs_dir = os.path.join("reports", "logs")
os.makedirs(logs_dir, exist_ok=True)
log_file = os.path.join(logs_dir, f"test_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")

logger = logging.getLogger("TestLogger")
logger.setLevel(logging.INFO)

# File handler
fh = logging.FileHandler(log_file)
fh.setLevel(logging.INFO)

# Console handler
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

# -------------------- Fixtures --------------------

@pytest.fixture(scope="session")
def config():
    return ReadConfig().get_config()

@pytest.fixture(scope="session")
def json_data():
    return read_json("config/testdata.json")

@pytest.fixture(scope="session")
def excel_data():
    return read_excel("config/test_data.xlsx", sheet_name="Sheet1")

@pytest.fixture(scope="session")
def csv_data():
    return read_csv("config/test_data.csv")

@pytest.fixture(scope="class")
def browsersetup(request, config):
    browser = request.config.getoption("--browser") or "chrome"
    headless = request.config.getoption("--headless") or False
    driver = BrowserFactory.get_driver(browser_name=browser, headless=headless)
    request.cls.driver = driver
    driver.get(config["base_url"])
    logger.info(f"Opened URL: {config['base_url']} in {browser} (headless={headless})")
    yield driver
    driver.quit()
    logger.info(f"Closed browser: {browser}")

# -------------------- CLI Options --------------------
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser: chrome, firefox, edge")
    parser.addoption("--headless", action="store_true", default=False, help="Run browser in headless mode")

# -------------------- Hook for Failure, Screenshots & Logs --------------------
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Capture screenshots on test failure, attach to HTML & Allure, and attach logs to Allure.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

    if rep.when == "call" and rep.failed:
        driver = getattr(item.instance, "driver", None)
        if driver:
            screenshots_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            file_path = os.path.join(
                screenshots_dir,
                f"{item.name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            )
            driver.save_screenshot(file_path)
            logger.error(f"Test '{item.name}' failed. Screenshot saved at {file_path}")

            # Attach to Allure
            if allure:
                with open(file_path, "rb") as f:
                    allure.attach(f.read(), name="Failure Screenshot",
                                  attachment_type=allure.attachment_type.PNG)
                # Attach log file to Allure
                with open(log_file, "r") as f:
                    allure.attach(f.read(), name="Test Log", attachment_type=allure.attachment_type.TEXT)

            # Attach to HTML report
            html_plugin = item.config.pluginmanager.getplugin("html")
            if html_plugin is not None:
                extra = getattr(rep, "extra", [])
                extra.append(html_plugin.extras.image(file_path))
                rep.extra = extra

# -------------------- Allure Automatic Steps --------------------
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    """Wrap each test function in an Allure step automatically"""
    if allure:
        with allure.step(f"Executing test: {item.name}"):
            yield
    else:
        yield
