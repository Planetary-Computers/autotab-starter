import time

from src.utils.driver import get_driver


def main():
    driver = get_driver()  # noqa: F841
    # Update this with e.g. logins to sites you want your
    # agent to always have access to
    # Agent code here...

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
