#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import requests
import requests_cache
from cStringIO import StringIO
from dateutil.parser import parse as parse_datetime
import datetime


def download_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return StringIO(response.content)


def parse_date(date_string, not_before=None):
    """
    >>> parse_date('03/07/2013')
    datetime.date(2013, 7, 3)
    >>> parse_date('3 January 2006', datetime.date(2006, 6, 1))
    datetime.date(2007, 1, 3)
    """
    parsed = parse_datetime(date_string, dayfirst=True).date()
    if not_before and parsed < not_before:
        parsed = datetime.date(
            1 + not_before.year,
            parsed.month,
            parsed.day)
    return parsed
