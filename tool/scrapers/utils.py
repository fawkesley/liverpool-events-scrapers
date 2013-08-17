#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import requests
import requests_cache
from cStringIO import StringIO
from dateutil.parser import parse as parse_datetime


def download_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return StringIO(response.content)


def parse_date(date_string):
    """
    >>> parse_date('03/07/2013')
    datetime.date(2013, 7, 3)
    """

    return parse_datetime(date_string, dayfirst=True).date()
