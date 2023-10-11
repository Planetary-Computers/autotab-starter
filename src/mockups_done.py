import argparse
import datetime
import os
import pathlib
import time
import zipfile
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from dotenv import load_dotenv
from selenium.webdriver.common.by import By

from src.site_agents.figma import download_figma_exports, get_sharing_link_for_flow
from src.site_agents.google import upload_files_to_folder
from src.site_agents.notion import append_image_to_notion_page
from src.utils.api import make_notion_request
from src.utils.config import config
from src.utils.env import get_env_escape_quotes
from src.utils.driver import get_driver
from src.utils.auth import login, google_login

load_dotenv()

NOTION_DB_ID = get_env_escape_quotes("NOTION_DB_ID")
CHROME_BINARY_LOCATION = get_env_escape_quotes("CHROME_BINARY_LOCATION")
GDRIVE_PARENT_FOLDER_URL = get_env_escape_quotes("GDRIVE_PARENT_FOLDER_URL")
NOTION_WORKSPACE = get_env_escape_quotes("NOTION_WORKSPACE")
NOTION_API_KEY = get_env_escape_quotes("NOTION_API_KEY")


def main(figma_link: str, company_name: str):
    print(
        f"Running mockups done (ready for review) automation for figma_link {figma_link} and company_name {company_name}"
    )
    driver = get_driver()

    login(driver, figma_link)

    figma_sharing_link = get_sharing_link_for_flow(figma_link, driver)

    # Replace params in Figma URL
    url_parts = urlparse(figma_sharing_link)
    query_params = parse_qs(url_parts.query)
    query_params.update(
        {
            "scaling": ["scale-down-width"],
            "viewport": ["100"],
            "node-id": ["38-2286"],
            "hide-ui": ["1"],
        }
    )

    new_query_string = urlencode(query_params, doseq=True)
    figma_sharing_link = urlunparse(
        (
            url_parts.scheme,
            url_parts.netloc,
            url_parts.path,
            url_parts.params,
            new_query_string,
            url_parts.fragment,
        )
    )

    driver.find_element_with_retry(
        By.CSS_SELECTOR, "[data-button-type='share']"
    ).click()
    time.sleep(1)
    figma_design_link = driver.execute_script("return navigator.clipboard.readText();")
    # Pretty sure this is identical to the input figma link?

    close_button = driver.find_element_with_retry(
        By.CLASS_NAME, "close_button--closeX--cA6xw"
    )
    close_button.click()
    time.sleep(1)

    download_figma_exports(figma_link, driver)

    # Unzip the download and rename the files
    downloads_dir = (
        "/tmp" if config.environment.is_container else os.path.expanduser("~/Downloads")
    )
    files = os.listdir(downloads_dir)
    zip_files = [
        f
        for f in files
        if f.endswith(".zip")
        and os.path.getmtime(os.path.join(downloads_dir, f))
        > (datetime.datetime.now() - datetime.timedelta(minutes=5)).timestamp()
    ]

    if not zip_files:
        raise Exception("No zip file downloaded in the last 5 minutes.")

    latest_zip_file = max(
        zip_files, key=lambda f: os.path.getmtime(os.path.join(downloads_dir, f))
    )
    with zipfile.ZipFile(os.path.join(downloads_dir, latest_zip_file), "r") as zip_ref:
        zip_ref.extractall(
            os.path.join(downloads_dir, latest_zip_file.replace(".zip", ""))
        )

    extracted_folder = pathlib.Path(downloads_dir) / pathlib.Path(latest_zip_file).stem
    png_files = list(extracted_folder.glob("*.png"))

    if len(png_files) != 2:
        print([f.name for f in png_files])
        raise Exception("Expected two png files in the extracted zip.")

    (extracted_folder / "Landing Page13.png").rename(
        extracted_folder / f"{company_name} Mockup 2x.png"
    )
    (extracted_folder / "Landing Page.png").rename(
        extracted_folder / f"{company_name} Mockup.png"
    )
    full_filepaths = [f for f in extracted_folder.glob("*.png")]

    # Go to GDrive, create the folder if it doesn't exist
    # Then upload the two image files
    google_login(driver)

    folder_name = company_name
    gdrive_folder_link = upload_files_to_folder(
        driver,
        GDRIVE_PARENT_FOLDER_URL,
        folder_name,
        full_filepaths,
    )

    # Update Notion
    data = {
        "filter": {
            "property": "Name",
            "rich_text": {"equals": company_name},
        }
    }
    response = make_notion_request(
        f"https://api.notion.com/v1/databases/{NOTION_DB_ID}/query",
        NOTION_API_KEY,
        method="POST",
        data=data,
    )
    if len(response["results"]) != 1:
        raise Exception("Expected exactly one result from Notion query.")

    notion_page_id = response["results"][0]["id"]
    page_url = f"https://api.notion.com/v1/pages/{notion_page_id}"

    update_data = {
        "properties": {
            "Drive Folder": {"type": "url", "url": gdrive_folder_link},
            "Figma Prototype": {"type": "url", "url": figma_sharing_link},
            "Figma Design": {"type": "url", "url": figma_design_link},
            "Status": {"type": "status", "status": {"name": "Ready for feedback"}},
        }
    }
    response = make_notion_request(page_url, NOTION_API_KEY, method="PATCH", data=update_data)

    # Add 1x mockup to Notion
    driver = get_driver()
    login(driver, "notion.so")

    image_filepath = [f for f in full_filepaths if "2x" not in f.name][0]
    append_image_to_notion_page(driver, NOTION_WORKSPACE, company_name, notion_page_id, image_filepath)

    driver.close()

    print("Finished updating Notion and Google Drive with the new mockups!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run the automation when mockups are done"
    )

    parser.add_argument(
        "FigmaLink", metavar="FigmaLink", type=str, help="the link to the Figma file"
    )
    parser.add_argument(
        "CompanyName", metavar="CompanyName", type=str, help="the name of the company"
    )

    args = parser.parse_args()
    

    # main(args.FigmaLink, args.CompanyName)
