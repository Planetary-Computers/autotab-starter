import json
import os
import time
from typing import Optional

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from utils.config import SiteCredentials, config
from utils.url_utils import extract_domain_from_url


def is_signed_in_to_google(driver):
    cookies = driver.get_cookies()
    return len([c for c in cookies if c["name"] == "SAPISID"]) != 0


def google_login(
    driver, credentials: Optional[SiteCredentials] = None, navigate: bool = True
):
    print("Logging in to Google")
    if navigate:
        driver.get("https://accounts.google.com/")
        time.sleep(1)
        if is_signed_in_to_google(driver):
            print("Already signed in to Google")
            return

    if os.path.exists("google_cookies.json"):
        print("cookies exist, doing loading")
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

    if not credentials:
        credentials = config.google_credentials.default

    if credentials is None:
        raise Exception("No credentials provided for Google login")

    email_input = driver.find_element(By.CSS_SELECTOR, "[type='email']")
    email_input.send_keys(credentials.email)
    email_input.send_keys(Keys.ENTER)
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "[type='password']"))
    )

    password_input = driver.find_element(By.CSS_SELECTOR, "[type='password']")
    password_input.send_keys(credentials.password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(1.5)
    print("Successfully logged in to Google")

    cookies = driver.get_cookies()
    if not is_signed_in_to_google(driver):
        # Probably wanted to have us solve a captcha, or 2FA or confirm recovery details
        print("Need 2FA help to log in to Google")
        # TODO: Show screenshot it to the user
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
            By.CSS_SELECTOR, f"[data-identifier='{credentials.email}']"
        )
        login_button.click()
        time.sleep(1)
        password_input = driver.find_element(By.CSS_SELECTOR, "[type='password']")
        password_input.send_keys(credentials.password)
        password_input.send_keys(Keys.ENTER)

        time.sleep(3)
        print("Successfully copied Google cookies for the future")


def login(driver, url: str):
    domain = extract_domain_from_url(url)

    credentials = config.get_site_credentials(domain)
    login_url = credentials.login_url
    if credentials.login_with_google_account:
        google_credentials = config.google_credentials.credentials[
            credentials.login_with_google_account
        ]
        _login_with_google(driver, login_url, google_credentials)
    else:
        _login(driver, login_url, credentials=credentials)


def _login(driver, url: str, credentials: SiteCredentials):
    print(f"Logging in to {url}")
    driver.get(url)
    time.sleep(2)
    email_input = driver.find_element(By.NAME, "email")
    email_input.send_keys(credentials.email)
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(credentials.password)
    password_input.send_keys(Keys.ENTER)

    time.sleep(3)
    print(f"Successfully logged in to {url}")


def _login_with_google(driver, url: str, google_credentials: SiteCredentials):
    print(f"Logging in to {url} with Google")

    google_login(driver, credentials=google_credentials)

    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body"))
    )

    main_window = driver.current_window_handle
    xpath = "//*[contains(text(), 'Continue with Google') or contains(text(), 'Sign in with Google') or contains(@title, 'Sign in with Google')]"

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
    driver.find_element(
        By.XPATH,
        xpath,
    ).click()

    driver.switch_to.window(driver.window_handles[-1])
    driver.find_element(
        By.XPATH, f"//*[contains(text(), '{google_credentials.email}')]"
    ).click()

    driver.switch_to.window(main_window)

    time.sleep(5)
    print(f"Successfully logged in to {url}")
