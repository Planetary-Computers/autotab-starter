import argparse

from typing import Optional

from selenium.webdriver.common.action_chains import ActionChains  # noqa: F401
from selenium.webdriver.common.by import By  # noqa: F401
from selenium.webdriver.common.keys import Keys  # noqa: F401
from selenium.webdriver.support import expected_conditions as EC  # noqa: F401
from selenium.webdriver.support.ui import WebDriverWait  # noqa: F401

from utils.auth import google_login, login  # noqa: F401
from utils.driver import get_driver
import utils.data as data  # noqa: F401


def main(data_filepath: Optional[str] = None):
    driver = get_driver()  # noqa: F841
    data.load(filepath=data_filepath)
    
    # Update this with e.g. logins to sites you want your
    # agent to always have access to
    # Ex. google_login(driver)
    # Ex. login(driver, "https://notion.so/")

    # Agent code here...
    data.get("username")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", help="Specify the data file path", default=None)
    args = parser.parse_args()
    main(data_filepath=args.data)
