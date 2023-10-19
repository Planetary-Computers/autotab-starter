from selenium.webdriver.common.action_chains import ActionChains  # noqa: F401
from selenium.webdriver.common.by import By  # noqa: F401
from selenium.webdriver.common.keys import Keys  # noqa: F401
from selenium.webdriver.support import expected_conditions as EC  # noqa: F401
from selenium.webdriver.support.ui import WebDriverWait  # noqa: F401

from src.utils.auth import google_login
from src.utils.driver import get_driver


def main():
    driver = get_driver()

    # Update this with e.g. logins to sites you want your
    # agent to always have access to
    google_login(driver)

    # Agent code here...


if __name__ == "__main__":
    main()
