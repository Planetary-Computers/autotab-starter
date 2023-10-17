FROM python:3.10-slim as build

# Install necessary packages and download Chrome and Chromedriver
RUN apt-get update && apt-get install -y curl unzip && \
    curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" && \
    curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1135561%2Fchrome-linux.zip?alt=media" && \
    unzip /tmp/chromedriver.zip -d /opt/ && \
    unzip /tmp/chrome-linux.zip -d /opt/ && \
    apt-get remove -y curl unzip && apt-get autoremove -y && apt-get clean

FROM python:3.10-slim

# Install necessary packages for Chrome
RUN apt-get update && apt-get install -y build-essential libxi6 libgconf-2-4 xvfb

# Install additional packages needed for Chrome and copy over from build step
RUN apt-get update && apt-get install -y \
    libatk1.0-0 libcups2 libgtk-3-0 libxcomposite1 libasound2 \
    libxcursor1 libxdamage1 libxext6 libxi6 libxrandr2 \
    libxss1 libxtst6 libpango-1.0-0 libatspi2.0-0 libxt6 \
    xvfb xauth libdbus-glib-1-2 libdbus-glib-1-dev \
    libx11-6 libx11-xcb1 libxfixes3 libxrender1 \
    libnss3 libxkbfile1 xdg-utils libappindicator1

COPY --from=build /opt/chrome-linux /opt/chrome
COPY --from=build /opt/chromedriver /opt/

# Upgrade pip and install requirements
RUN pip3 install --upgrade pip
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy source code and configuration file
COPY src src
COPY .autotab.yaml .autotab.yaml

# Set environment variable and command to run
ENV AUTOTAB_ENVIRONMENT=container
ARG FIGMA_URL
ARG COMPANY_NAME
CMD python -u -m src.mockups_done ${FIGMA_URL} ${COMPANY_NAME}
