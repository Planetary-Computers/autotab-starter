import os
from typing import Optional


def play(agent_name: Optional[str] = None, params_filepath: Optional[str] = None):
    if agent_name is None:
        agent_files = os.listdir("agents")
        if len(agent_files) == 0:
            raise Exception("No agents found in agents/ directory")
        elif len(agent_files) == 1:
            agent_file = agent_files[0]
        else:
            print("Found multiple agent files, please select one:")
            for i, file in enumerate(agent_files, start=1):
                print(f"{i}. {file}")

            selected = int(input("Select a file by number: ")) - 1
            agent_file = agent_files[selected]
    else:
        agent_file = f"{agent_name}.py"

    os.system(f"python agents/{agent_file} --data={params_filepath}")


if __name__ == "__main__":
    play()
