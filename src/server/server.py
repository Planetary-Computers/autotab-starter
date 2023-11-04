import json
from typing import Any, Dict, List, Optional

from fastapi import FastAPI
from IPython.core.interactiveshell import InteractiveShell
from pydantic import BaseModel

from utils.driver import AutotabChromeDriver

app = FastAPI()


class Session(BaseModel):
    shell: InteractiveShell
    cells: List[str] = []
    driver: Optional[AutotabChromeDriver] = None
    data_filepath: Optional[str] = None
    data: Optional[Dict[str, Any]] = None

    class Config:
        arbitrary_types_allowed = True

    def set_driver(self, driver: AutotabChromeDriver):
        self.driver = driver
        self.shell.push({"driver": self.driver})

    def setup_data(self, data_filepath: str):
        self.data_filepath = data_filepath
        if data_filepath is not None:
            with open(data_filepath) as f:
                self.data = json.load(f)

    def start(self):
        header = """from selenium.webdriver.common.action_chains import ActionChains  # noqa: F401
from selenium.webdriver.common.by import By  # noqa: F401
from selenium.webdriver.common.keys import Keys  # noqa: F401
from selenium.webdriver.support import expected_conditions as EC  # noqa: F401
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait  # noqa: F401

import utils.data as data

"""
        if self.data_filepath:
            header += f'data.load(filepath="{self.data_filepath}")\n'
        self.shell.run_cell(header)

    def reset(self):
        if self.driver:
            # Open a new tab
            self.driver.execute_script("window.open('');")
            # Switch to the new tab (it's the last one)
            self.driver.switch_to.window(self.driver.window_handles[-1])
            # Close all other tabs
            while len(self.driver.window_handles) > 1:
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.driver.close()
            # Switch back to the remaining tab
            self.driver.switch_to.window(self.driver.window_handles[0])

    def run(self, code: str | List[str]):
        if isinstance(code, list):
            for cell in code:
                self.shell.run_cell(cell)
        else:
            self.shell.run_cell(code)


session = Session(shell=InteractiveShell())

shell = InteractiveShell()


class Code(BaseModel):
    code: str


@app.post("/run_all")
def run_all(items: List[Code]):
    session.reset()
    session.run([item.code for item in items])
    return {"message": "Code executed successfully"}


@app.post("/run")
def run_code_block(item: Code):
    session.run(item.code)
    return {"message": "Code executed successfully"}


@app.get("/data")
def get_data():
    return session.data


def run_server(driver: AutotabChromeDriver, data_filepath: str):
    session.set_driver(driver)
    session.setup_data(data_filepath)
    session.start()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=1000)
