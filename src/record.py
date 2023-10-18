import os

from src.utils.auth import login
from src.utils.driver import get_driver


def record():
    driver = get_driver(record_mode=True)  # noqa: F841
    with open("src/template.py", "r") as file:
        data = file.read()
    if not os.path.exists("agents"):
        os.makedirs("agents")
    with open("agents/agent.py", "w") as file:
        file.write(data)
    login(driver, "https://www.figma.com")
    breakpoint()


if __name__ == "__main__":
    record()
