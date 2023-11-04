import time
from tempfile import mkdtemp
from typing import Optional, Tuple

import pyautogui
import requests
import undetected_chromedriver as uc  # type: ignore
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from extension import load_extension
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

    def open_plugin(self):
        print("Opening plugin sidepanel")
        self.execute_script("document.activeElement.blur();")
        pyautogui.press("esc")
        pyautogui.hotkey("command", "shift", "y", interval=0.05)  # mypy: ignore

    def open_plugin_and_login(self):
        if config.autotab_api_key is not None:
            backend_url = (
                "http://localhost:8000"
                if config.environment == "local"
                else "https://api.autotab.com"
            )
            self.get(f"{backend_url}/auth/signin-api-key-page")
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
            self.add_cookie(cookie)

            self.get("https://www.google.com")
            self.open_plugin()
        else:
            print("No autotab API key found, heading to autotab.com to sign up")

            url = (
                "http://localhost:3000/dashboard"
                if config.environment == "local"
                else "https://autotab.com/dashboard"
            )
            self.get(url)
            time.sleep(0.5)

            self.open_plugin()


def get_driver(
    autotab_ext_path: Optional[str] = None,
    include_ext: bool = True,
    headless: bool = False,
    window_size: Optional[Tuple[int, int]] = None,
) -> AutotabChromeDriver:
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")  # Necessary for running
    options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
    )
    options.add_argument("--enable-webgl")
    options.add_argument("--enable-3d-apis")
    options.add_argument("--enable-clipboard-read-write")
    options.add_argument("--disable-popup-blocking")

    if include_ext:
        if autotab_ext_path is None:
            load_extension()
            options.add_argument("--load-extension=./src/extension/autotab")
        else:
            options.add_argument(f"--load-extension={autotab_ext_path}")

    if window_size is not None:
        width, height = window_size
        options.add_argument(f"--window-size={width},{height}")

    if headless:
        options.add_argument("--headless")

    options.add_argument("--allow-running-insecure-content")
    options.add_argument("--disable-web-security")
    options.add_argument(f"--user-data-dir={mkdtemp()}")
    options.binary_location = config.chrome_binary_location

    driver = AutotabChromeDriver(options=options)

    if window_size is not None:
        width, height = window_size
        driver.set_window_size(width, height)

    return driver
