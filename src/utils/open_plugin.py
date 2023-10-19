import time

import pyautogui
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.auth import google_login
from src.utils.config import config


def open_plugin(driver):
    driver.execute_script("document.activeElement.blur();")
    pyautogui.press("esc")
    pyautogui.hotkey(["command", "shift", "y"], interval=0.05)
    time.sleep(1.5)


def open_plugin_and_login(driver):
    driver.get("https://google.com")
    time.sleep(1)

    open_plugin(driver)

    if config.autotab_credentials is not None:
        google_login(driver, config.autotab_credentials, navigate=True)

        pyautogui.hotkey(["command", "shift", "i"], interval=0.05)
        time.sleep(3)
        select_google_account(driver, config.autotab_credentials)
        time.sleep(0.5)
    else:
        print("Autotab credentials not found in config, skipping login to extension")


def select_google_account(driver, credentials):
    if len(driver.window_handles) == 1:
        open_plugin(driver)
        pyautogui.hotkey(["command", "shift", "i"], interval=0.05)

    driver.switch_to.window(driver.window_handles[1])

    try:
        xpath = f"//div[@data-identifier='{credentials.email}']"
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(0.7)
        return
    except Exception:
        pass

    try:
        xpath = f"//div[@data-email='{credentials.email}']"
        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.find_element(By.XPATH, xpath).click()
        time.sleep(0.7)
        return
    except Exception:
        print(f"Could not find account {credentials.email}")
