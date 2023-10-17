import time
from pathlib import Path
from tempfile import mkdtemp
from typing import Optional
import pyautogui

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.config import config
from src.utils.open_plugin import open_plugin


class AutotabChromeDriver(webdriver.Chrome):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_element_with_retry(
        self, by=By.ID, value: Optional[str] = None
    ) -> WebElement:
        try:
            return super().find_element(by, value)
        except Exception as e:
            # TODO: Use an LLM to retry, finding a similar element on the DOM
            breakpoint()
            raise e


def get_driver(autotab_ext_path: str = './src/extension/autotab.crx', record_mode: bool = False):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")  # Necessary for running
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.5938.92 Safari/537"
    )
    options.add_argument("--enable-webgl")
    options.add_argument("--enable-3d-apis")
    options.add_argument("--enable-clipboard-read-write")

    prefs = {"profile.default_content_setting_values.cookies": 1}
    if config.environment.is_container:
        prefs = {**prefs, "download.default_directory": "/tmp"}
    options.add_experimental_option("prefs", prefs)
    
    if autotab_ext_path:
        # options.add_extension(autotab_ext_path)
        
        # chrome_options.add_argument("user-data-dir=C:/Users/charl/OneDrive/python/userprofile/profilename"
        unpacked_extension_path = '/Users/alexirobbins/Sites/code/autotab/extension/build'
        options.add_argument('--load-extension={}'.format(unpacked_extension_path))
        
        # options.add_argument('load-extension=' + 'autotab')
        # options.add_argument('load-extension=' + autotab_ext_path)
        # driver.get("chrome-extension://"+autotab_ext_path+"/")

    if config.environment.is_container:
        # Display needed to render WebGL in headless mode
        display = Display(visible=0, size=(1920, 1080))
        display.start()

        options.add_argument("--headless")
        options.add_argument("--ignore-gpu-blacklist")
        # options.add_argument("--use-gl=swiftshader")
        # options.add_argument("--disable-gpu")  # Cannot disable because webGL for Figma
        options.binary_location = "/opt/chrome/chrome"
        options.add_argument("--window-size=1280x1696")
        options.add_argument("--single-process")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-web-security")
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        driver = AutotabChromeDriver("/opt/chromedriver", options=options)
    else:
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--disable-web-security")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        # options.add_argument("--incognito")
        options.binary_location = config.chrome_binary_location

        driver = AutotabChromeDriver(options=options)
    # EXTENSION_ID = 'opnpiohbfdicpkcokpijkhmijlepkkkl'
    # url = 'chrome-extension://{EXTENSION_ID}/src/sidepanel/index.html'.format(EXTENSION_ID=EXTENSION_ID)
    # driver.get(url)
    if record_mode:
        open_plugin(driver)
    
    return driver
