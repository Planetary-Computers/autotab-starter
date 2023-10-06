.PHONY: format

format:
	isort src && black src && flake8 src && mypy src

build-and-run:
	docker build --platform linux/amd64 -t scraper . && \
	docker run --platform linux/amd64 --env-file .env -v ./google_cookies.json:/var/task/google_cookies.json scraper


build-and-run-it:
	docker build --platform linux/amd64 -t scraper . && \
	docker run -it --platform linux/amd64 --entrypoint /bin/bash --env-file .env -v ./google_cookies.json:/var/task/google_cookies.json scraper
