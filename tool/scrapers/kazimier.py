#!/usr/bin/env python
# encoding: utf-8
from __future__ import unicode_literals

import logging
L = logging.getLogger('livlist.kazimier')

import lxml.html
from collections import OrderedDict
from utils import download_url, parse_date

BASE_URL = 'http://www.thekazimier.co.uk'

URL = BASE_URL + '/listings/'


def main():
    for row in process(download_url(URL)):
        yield row


def process(html_fobj):

    lxml_root = lxml.html.fromstring(html_fobj.read())
    divs = lxml_root.xpath('//div[@class="gif_box"]')
    assert len(divs) > 0

    earliest_date = None

    for div in divs:
        headline = clean_headline(div.xpath(
            './div[@class="gif_txt"]/a')[0].text_content().strip())

        url = div.xpath(
            './div/a/@href')[0]

        date_string = div.xpath(
            './div[@class="listdate"]')[0].text_content()

        if not earliest_date:
            earliest_date = parse_date(date_string)
        yield make_row(date_string, earliest_date, headline, url)


def clean_headline(headline):
    return headline


def make_row(date_string, earliest_date, headline, url):
    L.debug("'{}' : '{}'".format(headline, date_string))
    date = parse_date(date_string, not_before=earliest_date)
    L.debug("Parsed date '{}' as {}".format(date_string, date))
    return OrderedDict([
        ('venue', "Kazimier"),
        ('date', date),
        ('headline', headline),
        ('url', url)
    ])

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    for row in main():
        logging.info(row)
