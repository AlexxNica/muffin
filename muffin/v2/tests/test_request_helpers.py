# Copyright (C) Electronic Arts Inc.  All rights reserved.

import pytest
from muffin.v2.request_utils import get_customer_id, CustomerIdRequiredException, CustomerIdFormatException


class _Request:  # pylint: disable=too-few-public-methods
    def __init__(self, customer_id):
        self.headers = {"muffin-customer-id": customer_id}


def test_valid_customer_id():
    assert get_customer_id(_Request('00000000')) == 0
    assert get_customer_id(_Request('')) is None


def test_invalid_customer_id():
    with pytest.raises(CustomerIdFormatException):
        get_customer_id(_Request('foobar'))


def test_missing_customer_id():
    class RequestNoHeader:  # pylint: disable=too-few-public-methods
        def __init__(self):
            self.headers = {}

    with pytest.raises(CustomerIdRequiredException):
        get_customer_id(RequestNoHeader())
