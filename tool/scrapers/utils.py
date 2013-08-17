#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import requests
import requests_cache
from cStringIO import StringIO


def download_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return StringIO(response.content)
