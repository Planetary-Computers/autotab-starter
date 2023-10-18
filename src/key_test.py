from dotenv import load_dotenv
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from src.utils.driver import get_driver

load_dotenv()


def main():
    driver = get_driver()
    driver.get("https://www.google.com/")

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//textarea[@id='APjFqb']"))
    )
    search_field = driver.find_element(By.XPATH, "//textarea[@id='APjFqb']")
    search_field.click()
    driver.get("https://www.google.com/")

    actions = ActionChains(driver)
    actions.send_keys("a", "v", "o", "g", "a", "d", "r", "o", Keys.RETURN)

    actions.perform()
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, "//span[@class='FMKtTb UqcIvb' and contains(text(), 'Images')]")
        )
    )
    images_tab_link = driver.find_element(
        By.XPATH, "//span[@class='FMKtTb UqcIvb' and contains(text(), 'Images')]"
    )
    images_tab_link.click()


if __name__ == "__main__":
    main()
