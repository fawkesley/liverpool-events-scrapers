#!/usr/bin/env python
from __future__ import unicode_literals

import logging
L = logging.getLogger('livlist.philosophyinpubs')
import lxml.html
from collections import OrderedDict
import re
from utils import download_url, parse_date

BASE_URL = 'http://www.philosophyinpubs.org.uk'
VENUES_URL = BASE_URL + '/venues/all'
EVENTS_URL = BASE_URL + '/schedule/all'

VENUES_POSTCODES = {}  # venue id : postcode


def main():
    excluded_venues = get_excluded_venue_ids(download_url(VENUES_URL))

    for row in process(
            download_url(EVENTS_URL),
            exclude_venue_ids=excluded_venues):
        yield row


def get_excluded_venue_ids(venues_fobj):
    excluded = []
    lxml_root = lxml.html.fromstring(venues_fobj.read())
    table = lxml_root.xpath('//table[@class="venues"]')[0]
    trs = table.xpath('./tbody/tr')
    assert len(trs) > 0
    for tr in trs:
        if len(tr) == 1 and 'desc' in tr.attrib.get('class', ''):
            continue
        td_name, td_address, td_contact, td_schedule = tr
        address = td_address.text_content()
        postcode = _extract_postcode(address)
        venue_id = _venue_id_from_href(
            td_schedule.xpath('./a/@href')[0])
        if not _include_postcode(postcode):
            excluded.append(venue_id)

    return excluded


def _extract_postcode(address):
    """
    >>> _extract_postcode('Ranelagh Place, Liverpool (City Centre), L3 5UL')
    u'L3 5UL'
    >>> _extract_postcode('1 Church Street, Accrington, Lancashire, BB5 2EN')
    u'BB5 2EN'
    """

    return address.split(',')[-1].strip()


def _venue_id_from_href(href):
    """
    >>> _venue_id_from_href('/venues/view/80368a41d39457200d9ac01982e37e8e')
    u'80368a41d39457200d9ac01982e37e8e'
    """
    return href.split('/')[-1]


def _include_postcode(postcode):
    """
    >>> _include_postcode('L2 2JH')
    True
    >>> _include_postcode('L15 6LY')
    True
    >>> _include_postcode('LS2 6XX')
    False
    """
    is_liverpool = re.match(r'L\d+ .*', postcode) is not None
    if not is_liverpool:
        L.debug("Postcode '{}' is not Liverpool.".format(postcode))
    return is_liverpool


def process(html_fobj, excluded_venue_ids):
    lxml_root = lxml.html.fromstring(html_fobj.read())
    table = lxml_root.xpath('//table[@class="venues"]')[0]
    trs = table.xpath('./tbody/tr')
    assert len(trs) > 0
    for tr in trs:
        if len(tr) == 1 and 'desc' in tr.attrib.get('class', ''):
            continue
        row = _make_row_from_tr(tr, excluded_venue_ids)
        if row:
            yield row


def _make_row_from_tr(tr, excluded_venue_ids):
    (td_headline, td_venue, td_contact, td_date, td_time) = tr

    headline = td_headline.text_content()

    venue = clean_venue(td_venue.text_content())
    venue_id = _venue_id_from_href(td_venue.xpath('./a/@href')[0])
    if venue_id in excluded_venue_ids:
        L.info("Venue '{}' is in list of excluded ids.".format(venue))
        return

    url = BASE_URL + td_venue.xpath('./a/@href')[0]

    date_string = td_date.text_content()

    return make_row(date_string, headline, url, venue)


def clean_venue(venue):
    """
    >>> clean_venue('Foo (Liverpool)')
    u'Foo'
    >>> clean_venue('Foo (Allerton)')
    u'Foo (Allerton)'
    """
    if venue.endswith('(Liverpool)'):
        venue = venue.replace('(Liverpool)', '').strip()
    return venue.strip()


def clean_date(date_string):
    return re.sub('\s+', ' ', date_string).strip(' \n\r')


def is_date_range(date_string):
    """
    >>> is_date_range('Saturday, 07 Sep 2013 - Sunday, 08 Sep 2013 ')
    True
    >>> is_date_range('Thursday, 11 Jul 2013')
    False
    """
    return len(date_string.split(' ')) > 4


def make_row(date_string, headline, url, venue):
    date = parse_date(date_string)
    L.debug("Parsed date '{}' as {}".format(date_string, date))
    return OrderedDict([
        ('organiser', 'Philosophy In Pubs'),
        ('venue', venue),
        ('date', date),
        ('headline', headline),
        ('url', url)
    ])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    for row in main():
        logging.info(row)
