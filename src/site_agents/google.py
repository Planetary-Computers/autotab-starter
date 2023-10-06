import time
from pathlib import Path
from typing import List

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.utils.driver import ExtendedChromeDriver, find_element_with_retry


def upload_files_to_folder(
    driver: ExtendedChromeDriver,
    parent_folder_url: str,
    folder_name: str,
    local_file_paths: List[Path],
) -> str:
    driver.get(parent_folder_url)
    time.sleep(3)

    try:
        # No retry bc the folder not existing is a valid case
        existing_folder = driver.find_element(
            By.XPATH, f"//*[contains(text(), '{folder_name}')]"
        )
        assert (
            find_element_with_retry(existing_folder, By.XPATH, "..").get_attribute(
                "class"
            )
            == "bSmy5"
        )
    except Exception:
        new_menu_button = driver.find_element_with_retry(
            By.CSS_SELECTOR, "[guidedhelpid='new_menu_button']"
        )
        new_menu_button.click()
        time.sleep(2)
        new_folder_option = driver.find_element_with_retry(
            By.CSS_SELECTOR, "[data-tooltip='New folder']"
        )
        new_folder_option.click()
        time.sleep(2)

        input_field = driver.find_element_with_retry(
            By.CSS_SELECTOR, "[value='Untitled folder']"
        )
        input_field.clear()
        input_field.send_keys(folder_name)
        input_field.send_keys(Keys.ENTER)
        time.sleep(1)

    folders = driver.find_elements(By.CLASS_NAME, "bSmy5")
    target_folder = next(folder for folder in folders if folder_name in folder.text)

    action = webdriver.ActionChains(driver)
    action.double_click(target_folder).perform()
    time.sleep(3)

    gdrive_folder_link = driver.current_url

    for file_path in local_file_paths:
        original_file_inputs = driver.find_elements(By.CSS_SELECTOR, "[type='file']")

        new_menu_button = driver.find_element_with_retry(
            By.CSS_SELECTOR, "[guidedhelpid='new_menu_button']"
        )
        new_menu_button.click()
        time.sleep(1)

        new_file_option = driver.find_element_with_retry(
            By.CSS_SELECTOR, "[data-tooltip='File upload']"
        ).find_element(By.XPATH, "..")
        new_file_option.click()

        new_file_inputs = driver.find_elements(By.CSS_SELECTOR, "[type='file']")
        new_file_input = next(
            input for input in new_file_inputs if input not in original_file_inputs
        )
        new_file_input.send_keys(file_path.resolve().as_posix())
        time.sleep(1)
        try:
            # Happens if we are replacing a file
            upload_confirmation_showing = driver.find_element(
                By.XPATH, "//span[contains(text(), 'Upload')]"
            )
            upload_confirmation_showing.click()
            print("Replaced previous file with the same name")
        except NoSuchElementException:
            pass
        time.sleep(5)  # Let the upload happen
        print(f"Uploaded file {file_path.name} to Google Drive: {gdrive_folder_link}")

    driver.close()

    return gdrive_folder_link
