import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.utils.config import NOTION_WORKSPACE
from src.utils.driver import ExtendedChromeDriver, find_element_with_retry


def append_image_to_notion_page(
    driver: ExtendedChromeDriver,
    page_title: str,
    notion_page_id: str,
    image_filepath: Path,
):
    notion_url = f"https://www.notion.so/{NOTION_WORKSPACE}/{page_title}-{notion_page_id.replace('-', '')}"
    driver.get(notion_url)
    time.sleep(5)

    notion_frame = driver.find_element_with_retry(By.CLASS_NAME, "notion-frame")
    scroll_window = find_element_with_retry(
        notion_frame, By.CLASS_NAME, "notion-scroller"
    )

    # Scroll to the bottom of the scroll_window
    driver.execute_script(
        "arguments[0].scrollBy(0, arguments[0].scrollHeight);", scroll_window
    )
    time.sleep(1)

    # Click at the end of the content element
    content = find_element_with_retry(
        scroll_window, By.CLASS_NAME, "notion-page-content"
    )
    content_blocks = content.find_elements(By.XPATH, "./*")
    image_blocks = [
        block
        for block in content_blocks
        if "notion-image-block" in block.get_attribute("class")
    ]
    if len(image_blocks) == 1:
        print("Replacing previous image in Notion")
        last_block = image_blocks[0]
        action_chain = webdriver.ActionChains(driver)
        action_chain.send_keys(Keys.BACKSPACE).perform()
        content_blocks = content.find_elements(By.XPATH, "./*")

    last_block = content_blocks[-1]
    last_block.click()
    time.sleep(1)

    # Insert an image block
    action_chain = webdriver.ActionChains(driver)
    action_chain.key_down(Keys.ALT).send_keys(Keys.ARROW_RIGHT).key_up(
        Keys.ALT
    ).perform()
    time.sleep(1)
    action_chain.send_keys(Keys.ENTER)
    time.sleep(1)
    action_chain.send_keys("/image").send_keys(Keys.ENTER).perform()
    time.sleep(2)

    upload_file_button = driver.find_element_with_retry(
        By.XPATH, "//div[contains(text(), 'Upload file')]"
    )
    upload_file_button.click()

    # Find the image input element and upload the image
    image_input_element = next(
        element
        for element in driver.find_elements(By.CSS_SELECTOR, "[type='file']")
        if element.get_attribute("accept") == "image/*"
    )
    image_input_element.send_keys(image_filepath.resolve().as_posix())
    time.sleep(5)  # for upload to finish
