#!/usr/bin/env python

import logging
L = logging.getLogger('livlist.caledonia')
import lxml.html
from dateutil.parser import parse as parse_datetime
from collections import OrderedDict

from utils import download_url

URL = 'http://www.thecaledonialiverpool.com/whats-on/'


def main():
    for row in process(download_url(URL)):
        yield row


def process(html_fobj):
    lxml_root = lxml.html.fromstring(html_fobj.read())
    table = lxml_root.cssselect('table.table-whats-on')[0]
    trs = table.xpath('./tr')
    assert len(trs) > 0
    for tr in table:
        assert len(tr) == 2
        (th, td) = tr
        day = th.text_content()
        band_event = td.text_content()
        L.debug('{}: {}'.format(day, band_event))
        yield make_row(day, band_event)


def make_row(day, event):
    date = parse_datetime(day).date()
    L.debug("Parsed date '{}' as {}".format(day, date))
    return OrderedDict([
        ('venue', 'The Caledonia'),
        ('date', date),
        ('headline', event)])
