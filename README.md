# Automation

## Setup

### Installation

This scraper uses Chrome, if you want to use a different browser you will have to change the script. Chrome is assumed to be installed at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. If it isn't update `CHROME_BINARY_LOCATION` in the config.yaml file.

In addition to Chrome, Selenium requires `chromedriver` to run. On Mac, the easiest way to install chromedriver is with homebrew: `brew install chromedriver`.

Next, we need to install the Python dependencies. Create a virtual environment, then run `pip install -r requirements.txt`. If you also want to develop the code (in addition to running it) also run `pip install -r dev-requirements.txt`.

### Secrets

Create a .env file in the root folder with the variables listed in the .example.env file.

The first time the scraper logs in to Google might require 2FA based on your settings. The script will store the relevant cookies to avoid having to do 2FA every time. Note that those cookies are stored in a google_cookies.json file, which is sensitive (they would still need your password, but would no longer need 2FA).

The Notion setup is a bit more involved. You have to create a Notion integration, which you can do by following these steps: [Notion's Create a Integration Guide](https://developers.notion.com/docs/create-a-notion-integration). Finally, make sure to give the integration access to the relevant page in Notion (see guide above as well).

## Running the automation

After you have gone through all the installation steps above, you can simply run `python -m src.mockups_done <figma_url> <company_name>` from within your Python virtualenv, where `<figma_url>` is the link to the mockups project in Figma and `<company_name>` is the case-sensitive name of the company (used for the folder, file names & to find the Notion page).
