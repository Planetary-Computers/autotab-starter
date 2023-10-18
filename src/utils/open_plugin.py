import time

import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.auth import google_login
from src.utils.config import config


def open_plugin_and_login(driver):
    driver.get("https://google.com")
    time.sleep(1)
    pyautogui.hotkey(["command", "shift", "y"], interval=0.05)
    time.sleep(1.5)

    if config.autotab_credentials is not None:
        google_login(driver, config.autotab_credentials, navigate=True)

        pyautogui.hotkey(["command", "shift", "i"], interval=0.05)
        time.sleep(3)
        select_google_account(driver, config.autotab_credentials)
        time.sleep(0.5)
    else:
        print("Autotab credentials not found in config, skipping login to extension")


def select_google_account(driver, credentials):
    try:
        xpath = f"//div[@data-identifier='{credentials.email}']"
        driver.switch_to.window(driver.window_handles[1])
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f"{xpath}"))
        )
        driver.find_element(
            By.XPATH, f"{xpath}"
        ).click()
        time.sleep(0.7)
    except Exception as e:
        print(f"select login error: {e}")

