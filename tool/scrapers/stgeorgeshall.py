#!/usr/bin/env python

import logging
L = logging.getLogger('livlist.stgeorgeshall')
import lxml.html
from collections import OrderedDict
from utils import download_url, parse_date

URL = ('http://www.stgeorgesliverpool.co.uk/whatson/index.asp?'
       'cat=event&m=0&yr=0')


def main():
    for row in process(download_url(URL)):
        yield row


def process(html_fobj):
    lxml_root = lxml.html.fromstring(html_fobj.read())
    divs = lxml_root.cssselect('div.main_whatson')
    assert len(divs) > 0
    for div in divs:
        headline = div.xpath('./a')[0].text_content().strip()
        date_tag = div.xpath('./em[@class="date-time cf"]')[0]
        date_string = date_tag.text_content()
        if is_date_range(date_string):
            # Ignore events that are over a range of dates
            L.info("Ignoring event {} with date range {}".format(
                headline, date_string))
            continue
        L.debug("'{}' : '{}'".format(headline, date_string))
        yield make_row(date_string, headline)


def is_date_range(date_string):
    """
    >>> is_date_range('10 Aug - 01 Sep 13')
    True
    >>> is_date_range('03-18 Aug 13')
    True
    >>> is_date_range('12 Sep 13')
    False
    """
    if len(date_string.split(' ')) > 3:
        return True
    if '-' in date_string:
        return True

    return False


def clean_headline(headline):
    return headline


def make_row(date_string, headline):
    date = parse_date(date_string)
    L.debug("Parsed date '{}' as {}".format(date_string, date))
    return OrderedDict([
        ('venue', "St George's Hall"),
        ('date', date),
        ('headline', headline)])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    for row in main():
        logging.info(row)
