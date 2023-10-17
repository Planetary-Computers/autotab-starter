import argparse
import datetime
import os
import pathlib
import time
import zipfile
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from src.utils.config import config
from src.utils.driver import get_driver
from src.utils.auth import login, google_login


def play():
    # load_dotenv()
    # driver = get_driver()
    # # driver.get("https://www.google.com/")
    # Run the script at agents/agent.py
    os.system("python agents/agent.py")
    # while True:
    #     time.sleep(1)

if __name__ == "__main__":
    play()
