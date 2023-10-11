import os
import yaml

from typing import Optional, Dict, List
from pydantic import BaseModel
from enum import Enum

from src.utils.env import ENVIRONMENT

class Environment(str, Enum):
    LOCAL = 'local'
    CONTAINER = 'container'
    
    @property
    def is_container(self) -> bool:
        return self == Environment.CONTAINER

class SiteCredentials(BaseModel):
    password: Optional[str] = None
    email: Optional[str] = None
    login_with_google: Optional[bool] = False
    
class Config(BaseModel):
    default_email: str
    credentials: Dict[str, SiteCredentials]
    environment: Environment = Environment.LOCAL
    
    @classmethod
    def load_from_yaml(cls, path: str):
        with open(path, "r") as config_file:
            config = yaml.safe_load(config_file)
            _credentials = {}
            for creds in config.get("credentials", []):
                site_creds = SiteCredentials(**creds)
                for domain in creds['domains']:
                    _credentials[domain] = site_creds
                
            environment = config.get("environment", Environment.LOCAL)
            if ENVIRONMENT:
                environment = ENVIRONMENT
                
            return cls(
                environment=environment,
                default_email = config["default_email_address"],
                credentials = _credentials,
            )
    
    def get_site_credentials(self, url: str):
        credentials = self.credentials[url].copy()
        if not credentials.email:
            credentials.email = self.default_email
        return credentials
        

config = Config.load_from_yaml('.seedo.yaml')