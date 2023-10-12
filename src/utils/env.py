import os

from dotenv import load_dotenv

load_dotenv()


def get_env_escape_quotes(env_var):
    raw_value = os.getenv(env_var)
    if not raw_value:
        return raw_value
    if (raw_value.startswith('"') and raw_value.endswith('"')) or (
        raw_value.startswith("'") and raw_value.endswith("'")
    ):
        return raw_value[1:-1]
    return raw_value


SEEDO_ENVIRONMENT = get_env_escape_quotes("SEEDO_ENVIRONMENT")
