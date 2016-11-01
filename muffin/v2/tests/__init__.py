import json


def get_json(response):
    return json.loads(response.get_data(as_text=True))
