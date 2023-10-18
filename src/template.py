import time

from src.utils.driver import get_driver


def main():
    driver = get_driver()  # noqa: F841
    # Agent code here...

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
