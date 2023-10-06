# Browser Agents

## Quickstart

Want to get going quickly? It takes 5-10 minutes to get all the passwords and dependencies together so everything is set up.

1. Make sure Docker is installed. (1-5 minutes)
2. Create a file named `.env` with the keys from `.example.env` with values set. (1-2 minutes)
3. Update config.yaml (only the first section required). (~1 minute)
4. Setup done! Run `make build-run figma_url=<figma_url> company_name=<company_name>`

## Setup

### Installation

This scraper is designed to work with Chrome. If you wish to use a different browser, you will need to modify the script accordingly. The default location for Chrome is assumed to be `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. If your Chrome installation is located elsewhere, please update `CHROME_BINARY_LOCATION` in the config.yaml file.

In addition to Chrome, Selenium requires `chromedriver` to operate. On a Mac, you can easily install chromedriver using homebrew: `brew install chromedriver`.

Next, install the Python dependencies. First, create a virtual environment, then execute `pip install -r requirements.txt`. If you plan to modify the code in addition to running it, also execute `pip install -r dev-requirements.txt`.

### Secrets

Create a .env file in the root folder and populate it with the variables listed in the .example.env file.

The first time the scraper logs into Google, it may require 2FA depending on your settings. The script will store the relevant cookies to bypass 2FA in subsequent runs. Please note that these cookies are stored in a google_cookies.json file, which should be handled with care as it contains sensitive information.

Setting up Notion requires a few more steps. You need to create a Notion integration, which can be done by following these steps: [Notion's Create a Integration Guide](https://developers.notion.com/docs/create-a-notion-integration). Ensure that the integration has access to the relevant page in Notion.

Lastly, update `config.yaml` with the values that match your setup.

## Running the automation

The automation can be run either locally (where you can observe the automation in the browser - ideal for development and debugging) or remotely (suitable for high-volume runs and uninterrupted operation).

### Visible (local only)

After completing the installation steps above, you can run the automation locally by executing `python -m src.mockups_done <figma_url> <company_name>` within your Python virtual environment. Replace `<figma_url>` with the link to the mockups project in Figma and `<company_name>` with the exact name of the company (this is used for folder and file names, and to locate the Notion page). Make sure to put figma_url and company_name in quotes.

Ensure that the browser window controlled by the robot remains open and in focus, as certain applications may not render correctly otherwise, causing the automation to fail.

### Headless (local)

If you prefer not to have a browser window appear, but also don't want to set up a cloud environment, this option is ideal.

You will need Docker installed for this.

It is recommended to run it locally once (visible mode, see above) in order to have the google_cookies.json file created locally which can then be copied into the Docker container to avoid facing a 2FA challenge.

Then, execute `make build-run figma_url=<figma_url> company_name=<company_name>`, replacing the placeholders after the equals sign with the actual values. Make sure to put figma_url and company_name in quotes.

You can also run `make build-run-it` to run in headless mode inside the Docker container but interactively, which will allow you to run the script manually, set debug points etc. If you choose this, you will want to run `ENVIRONMENT=container python -m src.mockups_done <figma_url> <company_name>`. Make sure to put figma_url and company_name in quotes.

### Headless (remote)

Details on remote headless operation will be added soon.
