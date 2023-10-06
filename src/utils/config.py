import os

import yaml
from dotenv import load_dotenv

load_dotenv()


# Unfortunately Docker doesn't support env vars with quotes, so we have to do this
# https://github.com/docker/cli/issues/3630
def get_env_escape_quotes(env_var):
    raw_value = os.getenv(env_var)
    if (raw_value.startswith('"') and raw_value.endswith('"')) or (
        raw_value.startswith("'") and raw_value.endswith("'")
    ):
        return raw_value[1:-1]
    return raw_value


EMAIL = get_env_escape_quotes("EMAIL")
FIGMA_PASSWORD = get_env_escape_quotes("FIGMA_PASSWORD")
GOOGLE_PASSWORD = get_env_escape_quotes("GOOGLE_PASSWORD")
NOTION_API_KEY = get_env_escape_quotes("NOTION_API_KEY")
NOTION_PASSWORD = get_env_escape_quotes("NOTION_PASSWORD")

ENVIRONMENT = os.environ.get("ENVIRONMENT")

with open("config.yaml", "r") as config_file:
    config = yaml.safe_load(config_file)

NOTION_DB_ID = config["NOTION_DB_ID"]
CHROME_BINARY_LOCATION = config["CHROME_BINARY_LOCATION"]
GDRIVE_PARENT_FOLDER_URL = config["GDRIVE_PARENT_FOLDER_URL"]
NOTION_WORKSPACE = config["NOTION_WORKSPACE"]
