import os
import time

from src.utils.driver import get_driver


def record():
    get_driver(record_mode=True)
    with open("src/template.py", "r") as file:
        data = file.read()
    if not os.path.exists("agents"):
        os.makedirs("agents")
    with open("agents/agent.py", "w") as file:
        file.write(data)
    while True:
        time.sleep(1)


if __name__ == "__main__":
    record()
