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


class InvalidDbToObjectMappingException(MuffinError):  # pragma: no cover only thrown when code is incorrect
    def __init__(self, key, mapping, db_record):
        super().__init__(f"Invalid mapping '{mapping}' to key '{key}' db value was: {db_record}", status_code=500)


def get_common_params(request):
    fields = request.args.get('fields')
    if fields:
        fields = fields.split(',')

    per_page = request.args.get('per_page')

    return (fields, per_page)


def create_reference_to(name, endpoint_name, **values):
    return {'rel': name, 'url': flask.url_for(endpoint_name, **values)}


def apply_mapping_to_db_fields(fields, mapping):
    if not fields:
        return None

    db_fields = []
    for f in fields:
        x = mapping[f]
        if isinstance(x, list):
            db_fields.extend(x)
        else:
            db_fields.append(x)
    return db_fields


def map_db_record_to_dict(record, mapping, fields):
    all_fields = fields is None
    d = {}
    for k, v in mapping.items():
        if not all_fields and k not in fields:
            continue

        if callable(v):
            d[k] = v(record)
        elif v == "":

            if k not in record:
                continue
            rv = record[k]

            # forward the record value
            d[k] = rv
        else:  # pragma: no cover
            raise InvalidDbToObjectMappingException(k, v, rv)
    return d
