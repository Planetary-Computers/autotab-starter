import os
import shutil
import stat
import zipfile
from enum import Enum
from platform import architecture, machine, system
from typing import Optional

import requests
from pydantic import BaseModel, PrivateAttr
from tqdm import tqdm

CHROMIUM_BASE_URL = (
    "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/"
)
LOCAL_CHROMIUM_DIR = "./src/browser/chromium"


class OSName(Enum):
    MacIntel = "mac_intel"
    MacArm = "mac_arm"
    Windows = "win"
    Windows32 = "win32"
    Linux = "linux"
    Linux32 = "linux32"


def chmod_recursive(path):
    for root, dirs, files in os.walk(path):
        for file in files:
            os.chmod(os.path.join(root, file), stat.S_IREAD | stat.S_IEXEC)
        for dir in dirs:
            chmod_recursive(os.path.join(root, dir))


class OS(BaseModel):
    key: str
    chromium_filename: str
    chromium_appname: str
    chromedriver_filename: str
    chromedriver_appname: Optional[str] = "chromedriver"
    _latest_version: Optional[int] = PrivateAttr(None)

    @property
    def latest_version(self):
        if self._latest_version:
            return self._latest_version
        self._load_latest_version()
        return self._latest_version

    @property
    def chromium_filepath(self):
        return os.path.abspath(
            f"{LOCAL_CHROMIUM_DIR}/{self.chromium_filename}/{self.chromium_appname}"
        )

    @property
    def chromedriver_filepath(self):
        return os.path.abspath(
            f"{LOCAL_CHROMIUM_DIR}/{self.chromedriver_filename}/{self.chromedriver_appname}"
        )

    def _load_latest_version(self):
        url = f"{CHROMIUM_BASE_URL}{self.key}%2FLAST_CHANGE?alt=media"
        response = requests.get(url, stream=True)
        response.raise_for_status()
        for chunk in response.iter_lines():
            if chunk:
                self._latest_version = int(chunk.decode())
                return

    def _download_chromium(self):
        url = f"{CHROMIUM_BASE_URL}{self.key}%2F{self.latest_version}%2F{self.chromium_filename}.zip?alt=media"
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        with open(f"{LOCAL_CHROMIUM_DIR}/chromium.zip", "wb") as file:
            for data in tqdm(
                response.iter_content(block_size),
                total=total_size // block_size,
                unit="KB",
            ):
                file.write(data)
        with zipfile.ZipFile(f"{LOCAL_CHROMIUM_DIR}/chromium.zip", "r") as zip_ref:
            zip_ref.extractall(f"{LOCAL_CHROMIUM_DIR}/")
        os.chmod(self.chromium_filepath, stat.S_IRWXU)
        chmod_recursive(f"{LOCAL_CHROMIUM_DIR}/{self.chromium_filename}")

    def _download_chromedriver(self):
        url = f"{CHROMIUM_BASE_URL}{self.key}%2F{self.latest_version}%2F{self.chromedriver_filename}.zip?alt=media"
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1024
        with open(f"{LOCAL_CHROMIUM_DIR}/chromedriver.zip", "wb") as file:
            for data in tqdm(
                response.iter_content(block_size),
                total=total_size // block_size,
                unit="KB",
            ):
                file.write(data)
        with zipfile.ZipFile(f"{LOCAL_CHROMIUM_DIR}/chromedriver.zip", "r") as zip_ref:
            zip_ref.extractall(f"{LOCAL_CHROMIUM_DIR}/")
        os.chmod(self.chromedriver_filepath, stat.S_IRWXU)

    def download(self):
        if os.path.exists(LOCAL_CHROMIUM_DIR):
            shutil.rmtree(LOCAL_CHROMIUM_DIR)
        os.makedirs(LOCAL_CHROMIUM_DIR)
        print("downloading browser...")
        self._download_chromium()
        self._download_chromedriver()
        with open(f"{LOCAL_CHROMIUM_DIR}/LATEST_CHANGE.txt", "w") as file:
            file.write(str(self.latest_version))
        print("download complete")

    def should_update(self):
        try:
            with open(f"{LOCAL_CHROMIUM_DIR}/LATEST_CHANGE.txt", "r") as file:
                local_version = int(file.read())
        except FileNotFoundError:
            return True
        return local_version < self.latest_version


chromium_manager: Optional[OS] = None

os_lookup = {
    OSName.MacIntel: OS(
        key="Mac",
        chromium_filename="chrome-mac",
        chromium_appname="Chromium.app/Contents/MacOS/Chromium",
        chromedriver_filename="chromedriver_mac64",
    ),
    OSName.MacArm: OS(
        key="Mac_Arm",
        chromium_filename="chrome-mac",
        chromium_appname="Chromium.app/Contents/MacOS/Chromium",
        chromedriver_filename="chromedriver_mac64",
    ),
    OSName.Windows: OS(
        key="Win_x64",
        chromium_filename="chrome-win",
        chromium_appname="chrome.exe",
        chromedriver_filename="chromedriver_win32",
        chromedriver_appname="chromedriver.exe",
    ),
    OSName.Windows32: OS(
        key="Win",
        chromium_filename="chrome-win",
        chromium_appname="chrome.exe",
        chromedriver_filename="chromedriver_win32",
        chromedriver_appname="chromedriver.exe",
    ),
    OSName.Linux: OS(
        key="Linux_x64",
        chromium_filename="chrome-linux",
        chromium_appname="chrome",
        chromedriver_filename="chromedriver_linux64",
    ),
    OSName.Linux32: OS(
        key="Linux",
        chromium_filename="chrome-linux",
        chromium_appname="chrome",
        chromedriver_filename="NONE",
    ),
}


def get_os() -> OSName:
    os_name = system()
    if os_name == "Darwin":
        if machine() == "x86_64":
            return OSName.MacIntel
        elif machine() == "arm64":
            return OSName.MacArm
    elif os_name == "Windows":
        if architecture()[0] == "32bit":
            return OSName.Windows32
        else:
            return OSName.Windows
    elif os_name == "Linux":
        if architecture()[0] == "32bit":
            return OSName.Linux32
        else:
            return OSName.Linux
    raise ValueError("Unsupported OS")


def setup():
    global chromium_manager
    chromium_manager = os_lookup[get_os()]
    if chromium_manager.should_update():
        chromium_manager.download()


def get_manager() -> OS:
    global chromium_manager
    if chromium_manager is None:
        setup()
    assert chromium_manager is not None
    return chromium_manager


if __name__ == "__main__":
    global manager
    manager = os_lookup[get_os()]
    print("should os:", manager)
    print("should update:", manager.should_update())
    setup()
