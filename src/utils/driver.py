import time
from tempfile import mkdtemp
from typing import Optional

import pyautogui
import requests
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from utils.config import config


class AutotabChromeDriver(uc.Chrome):
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


def open_plugin_and_login(driver: AutotabChromeDriver):
    if config.autotab_api_key is not None:
        backend_url = (
            "http://localhost:8000"
            if config.environment == "local"
            else "https://api.autotab.com"
        )
        driver.get(f"{backend_url}/auth/signin-api-key-page")
        response = requests.post(
            f"{backend_url}/auth/signin-api-key",
            json={"api_key": config.autotab_api_key},
        )
        cookie = response.json()
        if response.status_code != 200:
            if response.status_code == 401:
                raise Exception("Invalid API key")
            else:
                raise Exception(
                    f"Error {response.status_code} from backend while logging you in with your API key: {response.text}"
                )
        cookie["name"] = cookie["key"]
        del cookie["key"]
        driver.add_cookie(cookie)
        driver.get("https://www.google.com")
    else:
        url = (
            "http://localhost:3000/dashboard"
            if config.environment == "local"
            else "https://autotab.com/dashboard"
        )
        driver.get(url)

    driver.execute_script("document.activeElement.blur();")
    pyautogui.press("esc")
    pyautogui.hotkey("command", "shift", "y", interval=0.05)
    time.sleep(1.5)


def get_driver(
    autotab_ext_path: Optional[str] = None, record_mode: bool = False
) -> AutotabChromeDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")  # Necessary for running
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )
    options.add_argument("--enable-webgl")
    options.add_argument("--enable-3d-apis")
    options.add_argument("--enable-clipboard-read-write")

    if autotab_ext_path is None:
        options.add_argument("--load-extension=./src/extension/autotab")
    else:
        options.add_argument(f"--load-extension={autotab_ext_path}")

    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-web-security")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.binary_location = config.chrome_binary_location

    driver = AutotabChromeDriver(options=options)

    if record_mode:
        open_plugin_and_login(driver)

    return driver
