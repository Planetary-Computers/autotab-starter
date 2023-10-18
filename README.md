# autotab Starter Repo

## Quickstart

It usually takes 5-10 minutes to get everything set up (including gathering passwords and installing dependencies). Follow these steps:

1. Create a new Python virtual environment and run `make install` to install all the dependencies. (~1 minute)
2. Install Google Chrome if you don't already have it installed. Then install chromedriver, which you can do with `brew install --cask chromedriver` on MacOS if you have homebrew installed. (~2 minutes)
3. Configure your credentials: Create a `.autotab.yaml` file following the example in `.example.autotab.yaml`. (~1 minute)
4. Setup done! Run `autotab record` to open a new browser window where you can start recording your actions.

## Setup

### Installation

See the quickstart above (Steps 1-3).

If you want to use a different browser that is not Chrome, you will need to modify the script accordingly. The location for Chrome is specified by `chrome_binary_location` in the `autotab.yaml` config file.

In addition to Chrome, Selenium requires `chromedriver` to operate. On a Mac, you can easily install chromedriver using homebrew: `brew install --cask chromedriver`.

Running `make install` installs all the dependencies and the local package which enables the `autotab record` and `autotab play` commands.

### Secrets

Create a `.autotab.yaml` file in the root folder and populate it with the variables listed in the `.example.autotab.yaml` file.

The first time an agent logs into Google, it may require 2FA depending on your settings. The script will store the relevant cookies to avoid 2FA in subsequent runs. Please note that these cookies are stored in a google_cookies.json file, which should be handled with care as it contains sensitive information (we store the logged-out cookies, so even if someone gets those cookies they still need your password to gain access).

## Running the automation

To run an automation, simply run `autotab play`. This will let you choose from the files in the agents/ folder and then run those.
