# autotab

Welcome to autotab! autotab makes it easy to create auditable browser automations using AI. Go from a point & click demonstration in the browser to immediately having code for those actions in seconds.

## Quickstart

It usually takes 5-10 minutes to get everything set up (including gathering passwords and installing dependencies). Follow these steps:

0. `git clone` this repository.
1. Create a new Python virtual environment and run `make install` to install all the dependencies. (~1 minute)
2. Install Google Chrome if you don't already have it installed. Then install chromedriver, which you can do with `brew install --cask chromedriver` on MacOS if you have homebrew installed. (~2 minutes)
3. Configure your credentials: Create a `.autotab.yaml` file following the example in `.example.autotab.yaml`. (~3 minutes)
4. Setup done! Run `autotab record` to open a new browser window where you can start recording your actions.

## Usage

### Recording an automation

To record a new automation, run `autotab record`. You can optionally add a `--agent <agent_name>` argument. This will launch a Chrome session controlled by Selenium and then log you in to Google and open the autotab extension in the sidepanel.

If the sidepanel does not open, type `Command - Shift - Y` to open the sidepanel.

Once the sidepanel is open, you can use record mode to record clicks and typing (`Command - E`) or select mode (`Command I`) to select an element to be hovered, copied to clipboard or to inject text into.

At the end of recording make sure to copy all the code. autotab will have created a `<agent_name>.py` file in the `agents/` folder with boilerplate code. Paste the code in there, format it and then your agent is ready to run!

### Running an automation

To play an automation you've already created, run `autotab play --agent <agent_name>`. Leaving out `--agent <agent_name>` has it default to run `agents/agent.py`. This just runs the Python script, so you can set debug as you would any other Python script. Often times interactions fail if the Chrome window running the automation isn't focused. We are working on a headless version that runs in the cloud which we hope to release soon to address this.

## Setup

### Installation

See the quickstart above (Steps 1 aand 2).

Running `make install` installs all the dependencies as well as the local package which enables the `autotab record` and `autotab play` commands.

### Secrets

Create a `.autotab.yaml` file in the root folder and populate it with the variables listed in the `.example.autotab.yaml` file.

The first time an agent logs into Google, it may require 2FA depending on your settings. The script will store the relevant cookies to avoid 2FA in subsequent runs. Please note that these cookies are stored in a google_cookies.json file, which should be handled with care as it contains sensitive information (we store only the logged-out cookies, so even if someone gets those cookies they still need your password to gain access).

## Disclaimer

This repository is provided as-is, with no guarantees. Before using any code, please review it thoroughly. If considering a scraper, familiarize yourself with the target website's guidelines and Terms of Service. Avoid any unauthorized or illegal activities. We hold no responsibility for any potential issues or outcomes.
