from enum import Enum
from typing import Dict, Optional

import yaml
from pydantic import BaseModel

from src.utils.env import AUTOTAB_ENVIRONMENT


class Environment(str, Enum):
    LOCAL = "local"
    CONTAINER = "container"

    @property
    def is_container(self) -> bool:
        return self == Environment.CONTAINER


class SiteCredentials(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    login_with_google: Optional[bool] = False
    login_url: Optional[str] = None


class Config(BaseModel):
    default_email: str
    credentials: Dict[str, SiteCredentials]
    environment: Environment = Environment.LOCAL
    chrome_binary_location: Optional[str] = None

    @classmethod
    def load_from_yaml(cls, path: str):
        with open(path, "r") as config_file:
            config = yaml.safe_load(config_file)
            _credentials = {}
            for creds in config.get("credentials", []):
                if "login_url" not in creds:
                    creds["login_url"] = f"https://{creds['domains'][0]}/login"
                site_creds = SiteCredentials(**creds)
                for domain in creds["domains"]:
                    _credentials[domain] = site_creds

            environment = config.get("environment", Environment.LOCAL)
            if AUTOTAB_ENVIRONMENT:
                # .env overrides yaml config
                environment = AUTOTAB_ENVIRONMENT

            return cls(
                default_email=config["default_email_address"],
                credentials=_credentials,
                environment=environment,
                chrome_binary_location=config.get("chrome_binary_location"),
            )

    def get_site_credentials(self, domain: str):
        credentials = self.credentials[domain].model_copy()
        if not credentials.email:
            credentials.email = self.default_email
        return credentials


config = Config.load_from_yaml(".autotab.yaml")
