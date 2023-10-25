from typing import List, Optional

from fastapi import FastAPI
from IPython.core.interactiveshell import InteractiveShell
from pydantic import BaseModel

from utils.driver import AutotabChromeDriver, get_driver

app = FastAPI()


class Session(BaseModel):
    shell: InteractiveShell
    cells: List[str] = []
    driver: Optional[AutotabChromeDriver] = None

    class Config:
        arbitrary_types_allowed = True

    def set_driver(self, driver: AutotabChromeDriver):
        self.driver = driver
        self.shell.push({"driver": self.driver})

    def start(self):
        header = """from selenium.webdriver.common.action_chains import ActionChains  # noqa: F401
from selenium.webdriver.common.by import By  # noqa: F401
from selenium.webdriver.common.keys import Keys  # noqa: F401
from selenium.webdriver.support import expected_conditions as EC  # noqa: F401
from selenium.webdriver.support.ui import WebDriverWait  # noqa: F401
"""
        self.shell.run_cell(header)

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
    session.run([item.code for item in items])
    return {"message": "Code executed successfully"}


@app.post("/run")
def run_code_block(item: Code):
    session.run(item.code)
    return {"message": "Code executed successfully"}


def run_server(driver: AutotabChromeDriver):
    _driver = get_driver(include_ext=False)
    session.set_driver(_driver)
    session.start()
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=1000)
