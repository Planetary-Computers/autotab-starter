from typing import Dict, Optional

import yaml
from pydantic import BaseModel


class SiteCredentials(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    login_with_google_account: Optional[str] = None
    login_url: Optional[str] = None

    def __init__(self, **data) -> None:
        super().__init__(**data)
        if self.name is None:
            self.name = self.email


class GoogleCredentials(BaseModel):
    credentials: Dict[str, SiteCredentials]

    def __init__(self, **data) -> None:
        super().__init__(**data)
        for cred in self.credentials.values():
            cred.login_url = "https://accounts.google.com/v3/signin"

    @property
    def default(self) -> SiteCredentials:
        if "default" not in self.credentials:
            if len(self.credentials) == 1:
                return list(self.credentials.values())[0]
            raise Exception("No default credentials found in config")
        return self.credentials["default"]


class Config(BaseModel):
    autotab_api_key: Optional[str]
    credentials: Dict[str, SiteCredentials]
    google_credentials: GoogleCredentials
    chrome_binary_location: str
    environment: str
    debug_mode: bool

    @classmethod
    def load_from_yaml(cls, path: str):
        with open(path, "r") as config_file:
            config = yaml.safe_load(config_file)
            _credentials = {}
            for domain, creds in config.get("credentials", {}).items():
                if "login_url" not in creds:
                    creds["login_url"] = f"https://{domain}/login"
                site_creds = SiteCredentials(**creds)
                _credentials[domain] = site_creds
                for alt in creds.get("alts", []):
                    _credentials[alt] = site_creds

            google_credentials = {}
            for creds in config.get("google_credentials", []):
                credentials: SiteCredentials = SiteCredentials(**creds)
                google_credentials[credentials.name] = credentials

            chrome_binary_location = config.get("chrome_binary_location")
            if chrome_binary_location is None:
                raise Exception("Must specify chrome_binary_location in config")

            autotab_api_key = config.get("autotab_api_key")
            if autotab_api_key == "...":
                autotab_api_key = None

            return cls(
                autotab_api_key=autotab_api_key,
                credentials=_credentials,
                google_credentials=GoogleCredentials(credentials=google_credentials),
                chrome_binary_location=config.get("chrome_binary_location"),
                environment=config.get("environment", "prod"),
                debug_mode=config.get("debug_mode", False),
            )

    def get_site_credentials(self, domain: str) -> SiteCredentials:
        credentials = self.credentials[domain].copy()
        return credentials


config = Config.load_from_yaml(".autotab.yaml")
