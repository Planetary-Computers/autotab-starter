from typing import Dict, Optional

import yaml
from pydantic import BaseModel


class SiteCredentials(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    login_with_google: Optional[bool] = False
    login_url: Optional[str] = None


class Config(BaseModel):
    autotab_email: Optional[str]
    autotab_password: Optional[str]
    default_email: str
    credentials: Dict[str, SiteCredentials]
    chrome_binary_location: str

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

            chrome_binary_location = config.get("chrome_binary_location")
            if chrome_binary_location is None:
                raise Exception("Must specify chrome_binary_location in config")

            return cls(
                autotab_email=config.get("autotab_email"),
                autotab_password=config.get("autotab_password"),
                default_email=config["default_email"],
                credentials=_credentials,
                chrome_binary_location=config.get("chrome_binary_location"),
            )

    def get_site_credentials(self, domain: str) -> SiteCredentials:
        credentials = self.credentials[domain].model_copy()
        if not credentials.email:
            credentials.email = self.default_email
        return credentials

    @property
    def autotab_credentials(self) -> Optional[SiteCredentials]:
        if self.autotab_email is None and self.autotab_password is None:
            return None
        return SiteCredentials(email=self.autotab_email, password=self.autotab_password)


config = Config.load_from_yaml(".autotab.yaml")
