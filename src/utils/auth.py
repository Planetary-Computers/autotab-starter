import json
import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.utils.config import SiteCredentials, config
from src.utils.url_utils import extract_domain_from_url


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

    credentials = config.get_site_credentials("google.com")
    email_input = driver.find_element(By.CSS_SELECTOR, "[type='email']")
    email_input.send_keys(credentials.email)
    email_input.send_keys(Keys.ENTER)
    time.sleep(3)
    password_input = driver.find_element(By.CSS_SELECTOR, "[type='password']")
    password_input.send_keys(credentials.password)
    password_input.send_keys(Keys.ENTER)
    time.sleep(3)
    print("Successfully logged in to Google")

    cookies = driver.get_cookies()
    if len([c for c in cookies if c["name"] == "SAPISID"]) == 0:
        # Probably wanted to have us solve a captcha, or 2FA or confirm recovery details
        print("Need 2FA help to log in to Google")
        # TODO: Show screenshot it to the user
        if config.environment.is_container:
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
    if credentials.login_with_google:
        _login_with_google(driver, login_url)
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


def _login_with_google(driver, url: str):
    print(f"Logging in to {url} with Google")

    google_login(driver)

    driver.get(url)
    time.sleep(2)

    main_window = driver.current_window_handle
    driver.find_element(
        By.XPATH, "//*[contains(text(), 'Continue with Google')]"
    ).click()

    driver.switch_to.window(driver.window_handles[-1])
    email = config.get_site_credentials("google.com").email
    driver.find_element(By.XPATH, f"//*[contains(text(), '{email}')]").click()

    driver.switch_to.window(main_window)

    time.sleep(5)
    print(f"Successfully logged in to {url}")
