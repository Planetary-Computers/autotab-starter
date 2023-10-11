import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from src.utils.config import config
from src.utils.driver import ExtendedChromeDriver, find_element_with_retry


def interactions_to_load(driver: ExtendedChromeDriver):
    # Take a screenshot to focus for loading WebGL
    # (needs access to display buffer)
    # Not needed inside Docker container
    if not config.environment.is_container:
        driver.get_screenshot_as_png()


def get_sharing_link_for_flow(figma_link: str, driver: ExtendedChromeDriver) -> str:
    print("Getting sharing link for flow in Figma")
    driver.get(figma_link)
    time.sleep(3)

    interactions_to_load(driver)

    actions = webdriver.ActionChains(driver)
    actions.key_down(Keys.COMMAND).key_down(Keys.SHIFT).send_keys("\\").key_up(
        Keys.COMMAND
    ).key_up(Keys.SHIFT).perform()
    time.sleep(3)

    elements_left_sidepanel = driver.find_element_with_retry(
        By.CLASS_NAME, "objects_panel--rowContainer--Y1-LY"
    )

    # Invariant: Because the flow and object are both called "Landing Page",
    # assume the flow element has no children
    flow_element_left_sidebar = find_element_with_retry(
        elements_left_sidepanel, By.CSS_SELECTOR, "[data-testid='layer-row']"
    )
    flow_element_left_sidebar.click()

    prototype_right_sidebar_button_div = driver.find_element_with_retry(
        By.CSS_SELECTOR, "[data-label='Prototype']"
    ).find_element(By.XPATH, "..")
    prototype_right_sidebar_button_div.click()
    time.sleep(2)

    properties_panel = driver.find_element_with_retry(
        By.CLASS_NAME, "properties_panel--propertiesPanel--gOq1f"
    )

    show_prototype_settings_button = find_element_with_retry(
        properties_panel,
        By.XPATH,
        "//button[contains(text(), 'Show prototype settings')]",
    )
    show_prototype_settings_button.click()
    time.sleep(2)

    # Need to hover for the copy element to be visible
    prototype_flow_panel_row = find_element_with_retry(
        properties_panel, By.CSS_SELECTOR, "[data-test-id='prototype-flow-panel-row']"
    )
    action = webdriver.ActionChains(driver)
    action.move_to_element(prototype_flow_panel_row).perform()
    time.sleep(1)

    copy_link_element = find_element_with_retry(
        prototype_flow_panel_row, By.CSS_SELECTOR, "[aria-label='Copy link']"
    )
    copy_link_element.click()
    time.sleep(1)
    driver.set_permissions("clipboard-read", "granted")
    figma_sharing_link = driver.execute_script("return navigator.clipboard.readText();")
    print(f"Got sharing link for flow in Figma: {figma_sharing_link}")
    return figma_sharing_link


def download_figma_exports(figma_link: str, driver: ExtendedChromeDriver):
    print("Downloading Figma exports")
    driver.get(figma_link)
    time.sleep(3)

    elements_left_sidepanel = driver.find_element_with_retry(
        By.CLASS_NAME, "objects_panel--rowContainer--Y1-LY"
    )

    landing_page_element_sidebar = find_element_with_retry(
        elements_left_sidepanel,
        By.CSS_SELECTOR,
        "[data-testid='layer-row-with-children']",
    )
    landing_page_element_sidebar.click()
    time.sleep(1)

    design_right_sidebar_button_div = driver.find_element_with_retry(
        By.CSS_SELECTOR, "[data-label='Design']"
    )
    action = webdriver.ActionChains(driver)
    action.move_to_element_with_offset(
        design_right_sidebar_button_div, 2, 2
    ).click().perform()
    time.sleep(1)

    properties_scroll_panel = driver.find_element_with_retry(
        By.ID, "properties-panel-scroll-container"
    )
    driver.execute_script("arguments[0].scrollTo(0, 100);", properties_scroll_panel)
    time.sleep(1)

    export_header = [
        t
        for t in driver.find_elements(
            By.CLASS_NAME, "draggable_list--panelTitleText--Bj2Hu"
        )
        if t.text == "Export"
    ][0]
    export_header.click()

    export_section_div = (
        find_element_with_retry(export_header, By.XPATH, "..")
        .find_element(By.XPATH, "..")
        .find_element(By.XPATH, "..")
        .find_element(By.XPATH, "..")
    )
    exports = export_section_div.find_elements(
        By.CLASS_NAME, "draggable_list--singleRow--0lcKt"
    )
    if len(exports) == 1:
        add_button = find_element_with_retry(
            export_section_div, By.CLASS_NAME, "draggable_list--addButton--9xznH"
        )
        add_button.click()
        time.sleep(1)

    export_2x_row, export_1x_row = export_section_div.find_elements(
        By.CLASS_NAME, "draggable_list--singleRow--0lcKt"
    )

    suffix_field = find_element_with_retry(
        export_2x_row, By.CSS_SELECTOR, "[placeholder='Suffix']"
    )
    suffix_field.clear()
    suffix_field.send_keys("13")

    export_button = driver.find_element_with_retry(
        By.XPATH, "//*[contains(text(), 'Export Landing Page')]"
    ).find_element(By.XPATH, "..")
    export_button.click()
    time.sleep(1)
    print("Finished downloading Figma exports")
