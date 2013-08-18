#!/usr/bin/env python

import logging
L = logging.getLogger('livlist.caledonia')
import lxml.html
from collections import OrderedDict

from utils import download_url, parse_date

URL = 'http://www.thecaledonialiverpool.com/whats-on/'


def main():
    for row in process(download_url(URL)):
        yield row


def process(html_fobj):
    lxml_root = lxml.html.fromstring(html_fobj.read())
    assert 1 == len(
        lxml_root.xpath('//p[contains(text(), "Live music for this month")]'))
    table = lxml_root.cssselect('table.table-whats-on')[0]
    trs = table.xpath('./tr')
    assert len(trs) > 0
    for tr in table:
        assert len(tr) == 2
        (th, td) = tr
        day = th.text_content()
        headline = 'Live Music: {}'.format(td.text_content())
        L.debug('{}: {}'.format(day, headline))
        yield make_row(day, headline)


def make_row(day, headline):
    date = parse_date(day)
    L.debug("Parsed date '{}' as {}".format(day, date))
    return OrderedDict([
        ('venue', 'The Caledonia'),
        ('date', date),
        ('headline', headline),
        ('url', 'http://www.thecaledonialiverpool.com/whats-on/'),
    ])
