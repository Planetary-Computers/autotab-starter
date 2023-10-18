from selenium.webdriver.common.by import By

from src.utils.auth import google_login
from src.utils.driver import get_driver


def main():
    driver = get_driver()
    google_login(driver)
    driver.get("https://mail.google.com/mail/u/0/#inbox")

    clicked_element = driver.find_element(
        By.XPATH, "//div[@id=':1v']/span/span[@name='SIMPLY GREEK']"
    )
    clicked_element.click()
    selectedElement = driver.find_element(
        By.XPATH, "//h2[@data-legacy-thread-id='18b3539c4f5fcbb3'][@class='hP']"
    )
    selectedElement = driver.find_element(
        By.XPATH,
        "//div[contains(@aria-label, 'Back to Inbox') and contains(@class, 'T-I J-J5-Ji lS T-I-ax7 mA T-I-JW T-I-JO T-I-Zf-aw2') and @role='button']",
    )
    selectedElement.click()


if __name__ == "__main__":
    main()
