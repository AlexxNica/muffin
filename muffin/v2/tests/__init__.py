# Copyright (C) Electronic Arts Inc.  All rights reserved.

import json


def get_json(response):  # pragma: no cover
    return json.loads(response.get_data(as_text=True))
