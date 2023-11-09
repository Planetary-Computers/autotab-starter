import os
import time
from multiprocessing import Process
from typing import Optional

from screeninfo import get_monitors

from mirror.mirror import mirror
from utils.config import config
from utils.driver import get_driver


def _is_blank_agent(agent_name: str) -> bool:
    with open(f"agents/{agent_name}.py", "r") as agent_file:
        agent_data = agent_file.read()
    with open("src/template.py", "r") as template_file:
        template_data = template_file.read()
    return agent_data == template_data


def record(
    agent_name: str,
    autotab_ext_path: Optional[str] = None,
    mirror_disabled: bool = False,
    params_filepath: Optional[str] = None,
):
    if not os.path.exists("agents"):
        os.makedirs("agents")

    if os.path.exists(f"agents/{agent_name}.py") and config.environment != "local":
        if not _is_blank_agent(agent_name=agent_name):
            raise Exception(f"Agent with name {agent_name} already exists")

    view_width, _ = get_monitors()[0].width, get_monitors()[0].height
    window_w = 3 / 4
    height_p = 0.65
    window_size = (int(view_width * window_w), int(view_width * window_w * height_p))
    if not mirror_disabled:
        p = Process(
            target=mirror,
            daemon=True,
            kwargs={
                "driver_window_size": window_size,
                "window_scaling_factor": (1 - window_w) / window_w,
                "left": window_size[0],
                "params_filepath": params_filepath,
            },
        )
        p.start()
        time.sleep(
            2
        )  # Wait for the mirror to open so we don't lose focus when opening the plugin

    driver = get_driver(  # noqa: F841
        autotab_ext_path=autotab_ext_path,
        window_size=window_size,
    )
    driver.set_window_position(0, 0)
    driver.open_plugin_and_login()

    with open("src/template.py", "r") as file:
        data = file.read()

    with open(f"agents/{agent_name}.py", "w") as file:
        file.write(data)

    if config.debug_mode:
        print(
            "\033[34mYou have the Python debugger open, you can run commands in it like you would in a normal Python shell.\033[0m"
        )
        print(
            "\033[34mTo exit, type 'q' and press enter. For a list of commands type '?' and press enter.\033[0m"
        )
        breakpoint()
    else:
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    record("agent")
