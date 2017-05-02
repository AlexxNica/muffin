# Copyright (C) Electronic Arts Inc.  All rights reserved.

import flask
from muffin.muffin_error import MuffinError


def get_customer_id(request):
    if "muffin-customer-id" not in request.headers:
        raise CustomerIdRequiredException

    customer_id = request.headers["muffin-customer-id"]
    if customer_id == '':
        return None

    try:
        return int(customer_id)
    except ValueError:
        raise CustomerIdFormatException


class CustomerIdRequiredException(MuffinError):
    def __init__(self):
        super().__init__("You have to specify a muffin-customer-id field")


class CustomerIdFormatException(MuffinError):
    def __init__(self):
        super().__init__("The muffin-customer-id field was not in a correct format")


def get_common_params(request):
    fields = request.args.get('fields')
    if fields:
        fields = fields.split(',')

    per_page = request.args.get('per_page')

    return (fields, per_page)


def create_reference_to(name, endpoint_name, **values):
    return {'rel': name, 'url': flask.url_for(endpoint_name, **values)}
