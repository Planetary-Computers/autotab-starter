## Update (Dec 12, 2023)

Thanks for trying out autotab! Over the last few weeks we’ve learned from so many of you and are excited to start rolling out a smoother and more user-friendly autotab V1 (no dependencies!).

As we transition, this repo will no longer be supported. The good news is that any Python code you’ve generated with autotab will of course work as usual.

Join our [Discord channel](https://discord.gg/seGGxSUgzM) to follow along and for a chance to be one of the first to try out new updates!

# autotab

Welcome to autotab! autotab makes it easy to create auditable browser automations using AI. Go from a point & click demonstration in the browser to live code for those actions in seconds.

> Note: This project is alpha release and actively being developed. Expect breaking changes and exciting new features regularly!

## Quickstart

It usually takes 5-10 minutes to get everything set up (including gathering passwords and installing dependencies). You must have the Chrome browser installed, and we recommend setting up a Python virtual environment:

```bash
git clone https://github.com/Planetary-Computers/autotab-starter.git
cd autotab-starter
# Recommended: Setup a Python virtual environment
make install
brew install --cask chromedriver
```

### Configuration

Configure your credentials: Create a `.autotab.yaml` file following the example in `.example.autotab.yaml`. (~3 minutes)

### Run

Run `autotab record` to open a new browser window where you can start recording your actions.

> Note: When you run `autotab record`, an automation will first try to log you in to autotab using the `autotab_api_key` from your `.autotab.yaml` file. You need to be logged in to autotab to use the extension (and our Open AI API key). You log in to `autotab record` using your autotab API key which you can get for free at [autotab.com/dashboard](https://autotab.com/dashboard).

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

See the quickstart above (Steps 1 and 2).

Running `make install` installs all the dependencies as well as the local package which enables the `autotab record` and `autotab play` commands.

### Secrets

Create a `.autotab.yaml` file in the root folder and populate it with the variables listed in the `.example.autotab.yaml` file.

The first time an agent logs into Google, it may require 2FA depending on your settings. The script will store the relevant cookies to avoid 2FA in subsequent runs. Please note that these cookies are stored in a google_cookies.json file, which should be handled with care as it contains sensitive information (we store only the logged-out cookies, so even if someone gets those cookies they still need your password to gain access).

## Disclaimer

This repository is provided as-is, with no guarantees. Before using any code, please review it thoroughly. If considering a scraper, familiarize yourself with the target website's guidelines and Terms of Service. Avoid any unauthorized or illegal activities. We hold no responsibility for any potential issues or outcomes.

> Note: By default autotab logs user data including the application state, DOM and model responses for recorded events while running `autotab record`. You can disable state and DOM logging by going to [Settings](https://www.autotab.com/dashboard/settings).
