from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional
from selenium import webdriver
from IPython.core.interactiveshell import InteractiveShell

app = FastAPI()

class Session(BaseModel):
    shell: InteractiveShell
    cells: List[str] = []
    driver: Optional[webdriver.Chrome] = None
    
    class Config:
        arbitrary_types_allowed = True
    
    def set_driver(self, driver: webdriver.Chrome):
        self.driver = driver
        self.shell.push({"driver": self.driver})
    
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

def run_server(driver: webdriver.Chrome):
    session.set_driver(driver)
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1000)