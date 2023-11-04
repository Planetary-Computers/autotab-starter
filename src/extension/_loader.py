import json
import os
import shutil
import xml.etree.ElementTree as ET
import zipfile

import requests
import semver
from tqdm import tqdm


def update():
    print("updating extension...")
    # Download the autotab.crx file
    response = requests.get(
        "https://github.com/Planetary-Computers/autotab-extension/raw/main/autotab.crx",
        stream=True,
    )

    # Check if the directory exists, if not create it
    if os.path.exists("src/extension/.autotab"):
        shutil.rmtree("src/extension/.autotab")
    os.makedirs("src/extension/.autotab")

    # Open the file in write binary mode
    total_size = int(response.headers.get("content-length", 0))
    block_size = 1024  # 1 Kibibyte
    t = tqdm(total=total_size, unit="iB", unit_scale=True)
    with open("src/extension/.autotab/autotab.crx", "wb") as f:
        for data in response.iter_content(block_size):
            t.update(len(data))
            f.write(data)
    t.close()
    if total_size != 0 and t.n != total_size:
        print("ERROR, something went wrong")

    # Unzip the file
    with zipfile.ZipFile("src/extension/.autotab/autotab.crx", "r") as zip_ref:
        zip_ref.extractall("src/extension/.autotab")
    os.remove("src/extension/.autotab/autotab.crx")
    if os.path.exists("src/extension/autotab"):
        shutil.rmtree("src/extension/autotab")
    os.rename("src/extension/.autotab", "src/extension/autotab")


def should_update():
    if not os.path.exists("src/extension/autotab"):
        return True
    # Fetch the XML file
    response = requests.get(
        "https://raw.githubusercontent.com/Planetary-Computers/autotab-extension/main/update.xml"
    )
    xml_content = response.content

    # Parse the XML file
    root = ET.fromstring(xml_content)
    namespaces = {"ns": "http://www.google.com/update2/response"}  # add namespaces
    xml_version = root.find(".//ns:app/ns:updatecheck", namespaces).get("version")

    # Load the local JSON file
    try:
        with open("src/extension/autotab/manifest.json", "r") as f:
            json_content = json.load(f)
        json_version = json_content["version"]
        # Compare versions
        return semver.compare(xml_version, json_version) > 0
    except FileNotFoundError:
        return True


def load_extension():
    should_update() and update()


if __name__ == "__main__":
    print("should update:", should_update())
    update()
