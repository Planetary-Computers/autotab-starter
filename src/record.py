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


def record():
    driver = get_driver(record_mode=True)
    with open('src/template.py', 'r') as file:
        data = file.read()
    if not os.path.exists('agents'):
        os.makedirs('agents')
    with open('agents/agent.py', 'w') as file:
        file.write(data)
    while True:
        time.sleep(1)

if __name__ == "__main__":
    record()
