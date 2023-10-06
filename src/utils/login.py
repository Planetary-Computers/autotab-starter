import json
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.utils.config import (
    EMAIL,
    ENVIRONMENT,
    FIGMA_PASSWORD,
    GOOGLE_PASSWORD,
    NOTION_PASSWORD,
)


def figma_login(driver):
    print("Logging in to Figma")
    driver.get("https://www.figma.com/login")
    time.sleep(2)

    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys(EMAIL)
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(FIGMA_PASSWORD)
    password_input.send_keys(Keys.ENTER)

    time.sleep(3)
    print("Successfully logged in to Figma")


def google_login(driver):
    print("Logging in to Google")
    driver.get(
        "https://accounts.google.com/v3/signin/identifier?continue=http%3A%2F%2Fdrive.google.com%2F%3Futm_source%3Den&ifkv=AYZoVhcdl5uTLa1Efje9aLyU2pr3EpjwRt4wwtepr_Lk7oaSb4MO0vq3gSYUOxyw2gtD6LYxTHfeug&ltmpl=drive&passive=true&service=wise&usp=gtd&utm_campaign=web&utm_content=gotodrive&utm_medium=button&flowName=GlifWebSignIn&flowEntry=ServiceLogin&dsh=S-1861333869%3A1696520938684040&theme=glif"
    )
    time.sleep(2)

    if os.path.exists("google_cookies.json"):
        with open("google_cookies.json", "r") as f:
            google_cookies = json.load(f)
            for cookie in google_cookies:
                if "expiry" in cookie:
                    cookie["expires"] = cookie["expiry"]
                    del cookie["expiry"]
                driver.execute_cdp_cmd("Network.setCookie", cookie)
            time.sleep(1)
            driver.refresh()
            time.sleep(2)

    email_input = driver.find_element(By.CSS_SELECTOR, "[type='email']")
    email_input.send_keys(EMAIL)
    email_input.send_keys(Keys.ENTER)
    time.sleep(3)
    password_input = driver.find_element(By.CSS_SELECTOR, "[type='password']")
    password_input.send_keys(GOOGLE_PASSWORD)
    password_input.send_keys(Keys.ENTER)
    time.sleep(3)
    print("Successfully logged in to Google")

    cookies = driver.get_cookies()
    if len([c for c in cookies if c["name"] == "SAPISID"]) == 0:
        # Probably wanted to have us solve a captcha, or 2FA or confirm recovery details
        print("Need 2FA help to log in to Google")
        # TODO: Show screenshot it to the user
        if ENVIRONMENT == "container":
            driver.get_screenshot_as_file("/var/task/2fa.png")
            time.sleep(30)  # Give time to solve 2FA
        else:
            breakpoint()

    if not os.path.exists("google_cookies.json"):
        print("Setting Google cookies for future use")
        # Log out to have access to the right cookies
        driver.get("https://accounts.google.com/Logout")
        time.sleep(2)
        cookies = driver.get_cookies()
        cookie_names = ["__Host-GAPS", "SMSV", "NID", "ACCOUNT_CHOOSER"]
        google_cookies = [
            cookie
            for cookie in cookies
            if cookie["domain"] in [".google.com", "accounts.google.com"]
            and cookie["name"] in cookie_names
        ]
        with open("google_cookies.json", "w") as f:
            json.dump(google_cookies, f)

        # Log back in
        login_button = driver.find_element(
            By.CSS_SELECTOR, f"[data-identifier='{EMAIL}']"
        )
        login_button.click()
        time.sleep(1)
        password_input = driver.find_element(By.CSS_SELECTOR, "[type='password']")
        password_input.send_keys(GOOGLE_PASSWORD)
        password_input.send_keys(Keys.ENTER)

        time.sleep(3)
        print("Successfully copied Google cookies for the future")


def notion_login(driver, use_google=False):
    print(f"Logging in to Notion {'with Google' if use_google else 'with password'}")
    # Google login is better if you run this frequently
    if use_google:
        google_login(driver)

    driver.get("https://www.notion.so/login")
    time.sleep(2)

    if use_google:
        main_window = driver.current_window_handle
        driver.find_element(
            By.XPATH, "//*[contains(text(), 'Continue with Google')]"
        ).click()

        driver.switch_to.window(driver.window_handles[-1])
        driver.find_element(By.XPATH, f"//*[contains(text(), '{EMAIL}')]").click()

        driver.switch_to.window(main_window)
    else:
        email_input = driver.find_element(By.CSS_SELECTOR, "[type='email']")
        email_input.send_keys(EMAIL)
        email_input.send_keys(Keys.ENTER)
        time.sleep(1)

        password_input = driver.find_element(By.CSS_SELECTOR, "[type='password']")
        password_input.send_keys(NOTION_PASSWORD)
        password_input.send_keys(Keys.ENTER)

    time.sleep(5)
    print("Successfully logged in to Notion")
