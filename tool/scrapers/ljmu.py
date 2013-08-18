#!/usr/bin/env python
from __future__ import unicode_literals

import logging
L = logging.getLogger('livlist.ljmu')
import lxml.html
from collections import OrderedDict
from utils import download_url, parse_date
import re

BASE_URL = 'http://www.ljmu.ac.uk'
URL = BASE_URL + '/events/'


def main():
    for row in process(download_url(URL)):
        yield row


def process(html_fobj):
    lxml_root = lxml.html.fromstring(html_fobj.read())
    tables = lxml_root.xpath(
        '//h2[contains(text(), "Forthcoming")]/ancestor::table')
    assert len(tables) == 1, "Found {} matching tables".format(len(tables))

    earliest_date = None
    for i, tr in enumerate(tables[0].xpath('./tbody/tr')):
        if len(tr) == 1 and i == 0:
            continue
        assert len(tr) == 3, "<tr> had {} subtags tags".format(len(tr))
        (td_headline_speaker, td_date_venue, td_ticket) = tr
        headline = td_headline_speaker.xpath(
            './p/strong')[0].text_content().strip()

        date_string = extract_date(
            td_date_venue.xpath('./p[1]')[0].text_content())
        venue = td_date_venue.xpath('./p[2]')[0].text_content()

        url = td_ticket.xpath('.//a/@href')[0]
        if not earliest_date:
            earliest_date = parse_date(date_string)
        yield make_row(date_string, earliest_date, headline, url, venue)


def extract_date(date_string):
    """
    >>> extract_date('Thursday 28 November, 6pm')
    u'Thursday 28 November'
    >>> extract_date('Thursday 5 September 2013 6.30pm - 8pm')
    u'Thursday 5 September 2013'
    """

    date_string = re.sub(r'[0-9.]+pm', '', date_string)
    date_string = date_string.rstrip('-, ')
    return date_string


def clean_headline(headline):
    return re.sub('\s+ ', ' ', headline)


def make_row(date_string, earliest_date, headline, url, venue):
    L.debug("'{}' : '{}'".format(headline, date_string))
    date = parse_date(date_string, not_before=earliest_date)
    L.debug("Parsed date '{}' as {}".format(date_string, date))
    return OrderedDict([
        ('organiser', "LJMU"),
        ('venue', venue),
        ('date', date),
        ('headline', headline),
        ('url', url),
    ])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    for row in main():
        logging.info(row)
