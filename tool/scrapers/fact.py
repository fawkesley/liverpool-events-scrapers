#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import logging
L = logging.getLogger('livlist.fact')

import re
import lxml.html
from collections import OrderedDict
from utils import download_url, parse_date

BASE_URL = 'http://www.fact.co.uk'
URL = BASE_URL + '/whats-on/?range=comingsoon'


def main():
    for row in process(download_url(URL)):
        yield row


def process(html_fobj):
    for row in get_all_listings(html_fobj):
        event_page = download_url(row['url'])

        if not is_single_event(event_page):
            L.info("Ignoring repeated event '{}'".format(row['headline']))
            continue

        event_page.seek(0)
        if is_child_event(event_page):
            L.info("Ignoring children's film '{}'".format(row['headline']))
            continue

        # TODO: row['description'] = parse_description(event_page)
        yield row


def get_all_listings(listings_fobj):
    lxml_root = lxml.html.fromstring(listings_fobj.read())
    divs = lxml_root.xpath('//div[@id="events_list"]/div[@class="item"]')
    assert len(divs) > 0

    earliest_date = None

    for div in divs:
        headline = clean_headline(
            div.xpath('./h4/a')[0].text_content().strip())

        url = BASE_URL + div.xpath('./h4/a/@href')[0]
        date_tag = div.xpath('./span[@class="from"]')[0]
        date_string = extract_date(date_tag.text_content())

        if not earliest_date:
            earliest_date = parse_date(date_string)
        yield make_row(date_string, earliest_date, headline, url)


def is_child_event(event_fobj):
    lxml_root = lxml.html.fromstring(event_fobj.read())
    try:
        rating = lxml_root.xpath(
            '//p[@class="film_details"]/img[@alt]/@alt')[0]
    except IndexError:
        L.debug("No certficiate, assuming not a child's event")
        return False
    return rating == 'U'


def is_single_event(event_fobj):
    """
    See whether the event page has exactly one showing time.
    """
    lxml_root = lxml.html.fromstring(event_fobj.read())
    return len(lxml_root.xpath(
        '//div[@class="times"]//a[@class="action"]')) == 1


def extract_date(showing_from_string):
    """
    >>> extract_date('Showing from: Monday 19 August')
    u'Monday 19 August'
    """
    return showing_from_string.replace('Showing from: ', '')


def clean_headline(headline):
    """
    Replace multiple whitespace with a single space
    >>> clean_headline('foo\\n\\rbar')
    u'foo bar'
    >>> clean_headline('Rush (15)')
    u'Rush'
    >>> clean_headline('My Neighbour Totoro (Subtitled) (U)')
    u'My Neighbour Totoro (Subtitled)'
    """
    headline = re.sub(r'\s+', ' ', headline)
    match = re.match(r'.*(?P<cert> \(.+\))', headline)
    if match:
        headline = headline.replace(match.group('cert'), '')
    return headline


def make_row(date_string, earliest_date, headline, url):
    L.debug("'{}' : '{}'".format(headline, date_string))
    date = parse_date(date_string, not_before=earliest_date)
    L.debug("Parsed date '{}' as {}".format(date_string, date))
    return OrderedDict([
        ('venue', "FACT"),
        ('date', date),
        ('headline', headline),
        ('url', url)
    ])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    for row in main():
        logging.info(row)
