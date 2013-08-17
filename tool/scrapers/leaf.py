#!/usr/bin/env python

import logging
L = logging.getLogger('livlist.caledonia')
import lxml.html
from collections import OrderedDict

from utils import download_url, parse_date

URL = 'http://thisisleaf.co.uk/on-bold-street/events/'


def main():
    for row in process(download_url(URL)):
        yield row


def process(html_fobj):
    lxml_root = lxml.html.fromstring(html_fobj.read())
    h3s = lxml_root.xpath('//h3')
    for h3 in h3s:
        headline = h3.text_content()
        p_tag_date = h3.xpath('./following-sibling::p[@class="caption"][1]')[0]
        date_string = p_tag_date.text_content()
        #L.debug("No p<class='caption'> under this h3")
        L.debug("'{}' : '{}'".format(headline, date_string))
        yield make_row(date_string, headline)


def make_row(date_string, headline):
    date = parse_date(date_string)
    L.debug("Parsed date '{}' as {}".format(date_string, date))
    return OrderedDict([
        ('venue', 'LEAF on Bold Street'),
        ('date', date),
        ('headline', headline)])
