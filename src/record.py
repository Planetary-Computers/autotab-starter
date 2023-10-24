import os
from typing import Optional

from dotenv import load_dotenv

from utils.driver import get_driver

load_dotenv()


def record(agent_name: str, autotab_ext_path: Optional[str] = None):
    driver = get_driver(  # noqa: F841
        autotab_ext_path=autotab_ext_path,
        record_mode=True,
    )
    # Need to keep a reference to the driver so that it doesn't get garbage collected
    with open("src/template.py", "r") as file:
        data = file.read()
    if not os.path.exists("agents"):
        os.makedirs("agents")
    if os.path.exists(f"agents/{agent_name}.py"):
        raise Exception(f"Agent with name {agent_name} already exists")
    with open(f"agents/{agent_name}.py", "w") as file:
        file.write(data)

    print(
        "\033[34mYou have the Python debugger open, you can run commands in it like you would in a normal Python shell.\033[0m"
    )
    print(
        "\033[34mTo exit, type 'q' and press enter. For a list of commands type '?' and press enter.\033[0m"
    )
    breakpoint()


if __name__ == "__main__":
    record("agent")
