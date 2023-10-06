import requests

from src.utils.config import NOTION_API_KEY


def make_notion_request(url, method="GET", data=None):
    headers = {
        "Authorization": "Bearer " + NOTION_API_KEY,
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    response = requests.request(method=method, url=url, headers=headers, json=data)
    try:
        response.raise_for_status()
    except Exception as e:
        print("Error when calling Notion API")
        print(response.text)
        raise e
    return response.json()
