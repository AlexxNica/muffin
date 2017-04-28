# Copyright (C) Electronic Arts Inc.  All rights reserved.

import flask


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


class CustomerIdRequiredException(Exception):
    def __init__(self):
        super().__init__(self)


class CustomerIdFormatException(Exception):
    def __init__(self):
        super().__init__(self)


def get_common_params(request):
    fields = request.args.get('fields')
    if fields:
        fields = fields.split(',')

    per_page = request.args.get('per_page')

    return (fields, per_page)


def create_reference_to(name, endpoint_name, **values):
    return {'rel': name, 'url': flask.url_for(endpoint_name, **values)}
