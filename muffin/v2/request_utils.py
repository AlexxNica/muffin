# Copyright (C) Electronic Arts Inc.  All rights reserved.

import flask


def get_customer_id(request):
    if "muffin-customer-id" not in request.headers:
        raise CustomerIdRequiredException

    customer_id = request.headers["muffin-customer-id"]
    if customer_id == '':
        return None
    return int(customer_id)

class CustomerIdRequiredException(Exception):
    def __init__(self):
        super().__init__(self)


def create_reference_to(name, endpoint_name, **values):
    return {'rel': name, 'url': flask.url_for(endpoint_name, **values)}
 