from pathlib import Path
from tempfile import mkdtemp
from typing import Optional

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

from src.utils.config import config


def get_driver_from_element(element: WebElement) -> WebDriver:
    parent = element.parent
    while not isinstance(parent, WebDriver):
        parent = parent.parent
    return parent


def find_element_with_retry(
    root_element: WebElement, by=By.ID, value: Optional[str] = None
):
    try:
        return root_element.find_element(by, value)
    except Exception as e:
        print(e)
        print(root_element.get_attribute("outerHTML"))
        print(root_element.get_attribute("innerHTML"))
        driver = get_driver_from_element(root_element)
        screenshot_path = (
            "/var/task/screenshot.png"
            if config.environment.is_container
            else str(Path.home() / "Desktop" / "screenshot.png")
        )
        driver.get_screenshot_as_file(screenshot_path)
        breakpoint()


class ExtendedChromeDriver(webdriver.Chrome):
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


def get_driver():
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
        options.add_argument("--no-zygote")
        options.add_argument(f"--user-data-dir={mkdtemp()}")
        options.add_argument(f"--data-path={mkdtemp()}")
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")
        options.add_argument("--remote-debugging-port=9222")
        driver = ExtendedChromeDriver("/opt/chromedriver", options=options)
    else:
        options.binary_location = config.chrome_binary_location

        driver = ExtendedChromeDriver(options=options)

    return driver
