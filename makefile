.PHONY: format

install:
	pip install -r requirements.txt &&\
	pip install -r dev-requirements.txt &&\
	pip install -e .

format:
	isort src && black src && flake8 src && mypy src

build:
	docker build --platform linux/amd64 -t scraper .

build-run:
	make build && \
	docker run --platform linux/amd64 --env-file .env -v ./google_cookies.json:/app/google_cookies.json -e FIGMA_URL="$(figma_url)" -e COMPANY_NAME="$(company_name)" scraper


build-run-it:
	make build && \
	docker run -it --entrypoint /bin/bash --platform linux/amd64 --env-file .env -v ./google_cookies.json:/app/google_cookies.json scraper
