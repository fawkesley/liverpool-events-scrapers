#!/usr/bin/env python

import logging
L = logging.getLogger('livlist.bluecoat')
import lxml.html
from collections import OrderedDict
import re
from utils import download_url, parse_date

URL = 'http://www.thebluecoat.org.uk/events/show/events'


def main():
    for row in process(download_url(URL)):
        yield row


def process(html_fobj):
    lxml_root = lxml.html.fromstring(html_fobj.read())
    divs = lxml_root.xpath('//div[@class="panel-wrapper"]/div')
    assert len(divs) > 0
    for div in divs:
        headline = div.xpath('./img[@alt]/@alt')[0]
        date_string = clean_date(div.xpath(
            './/p[@class="date"]')[0].text_content())
        if is_date_range(date_string):
            L.info("Excluding date range event '{}'".format(headline))
            continue
        url = div.xpath('.//div[@class="action"]/p/a/@href')[0]
        yield make_row(date_string, headline, url)


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


def make_row(date_string, headline, url):
    date = parse_date(date_string)
    L.debug("Parsed date '{}' as {}".format(date_string, date))
    return OrderedDict([
        ('organiser', 'The Bluecoat'),
        ('venue', 'The Bluecoat'),
        ('date', date),
        ('headline', headline),
        ('url', url)
    ])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    for row in main():
        logging.info(row)
