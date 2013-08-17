#!/usr/bin/env python

import logging
L = logging.getLogger('livlist.leaf')
import lxml.html
from collections import OrderedDict
import re
from utils import download_url, parse_date

URL = 'http://thisisleaf.co.uk/on-bold-street/events/'


def main():
    for row in process(download_url(URL)):
        yield row


def process(html_fobj):
    lxml_root = lxml.html.fromstring(html_fobj.read())
    h3s = lxml_root.xpath('//h3')
    for h3 in h3s:
        headline = clean_headline(h3.text_content())
        p_tag_date = h3.xpath('./following-sibling::p[@class="caption"][1]')[0]
        date_string = p_tag_date.text_content()
        #L.debug("No p<class='caption'> under this h3")
        L.debug("'{}' : '{}'".format(headline, date_string))
        yield make_row(date_string, headline)


def clean_headline(headline):
    """
    Headlines often end with some sort of date modifier. Remove these.
    >>> clean_headline('foo August 2013')
    'foo'
    >>> clean_headline('foo - July')
    'foo'
    """
    headline = headline.rstrip()
    match = re.match(r'.*(?P<year>\d\d\d\d)', headline)
    if match and match.group('year').startswith('20'):
        headline = headline[0:-4].rstrip()

    months = set(['january', 'february', 'march', 'april', 'may', 'june',
                  'july', 'august', 'september', 'october', 'november',
                  'december'])

    for month in months:
        if headline.lower().endswith(month):
            headline = headline[0:-len(month)].rstrip(' -,')
    return headline


def make_row(date_string, headline):
    date = parse_date(date_string)
    L.debug("Parsed date '{}' as {}".format(date_string, date))
    return OrderedDict([
        ('venue', 'LEAF on Bold Street'),
        ('date', date),
        ('headline', headline)])
