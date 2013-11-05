#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals
import sys
import codecs
import requests
import requests_cache
from collections import OrderedDict
from cStringIO import StringIO
import datetime
import scraperwiki
import logging

import scrapers


UNIQUE_KEYS = ['venue', 'date', 'headline']


def main():
    logging.basicConfig(level=logging.DEBUG)
    install_cache()

    #for row in scrapers.ljmu.main():
    #    save_row(row)

    for row in scrapers.stgeorgeshall.main():
        save_row(row)

    for row in scrapers.bluecoat.main():
        save_row(row)

    for row in scrapers.philosophyinpubs.main():
        save_row(row)

    #for row in scrapers.leaf.main():
    #    save_row(row)

    #for row in scrapers.fact.main():
    #    save_row(row, table_name='film_and_theatre')

    #for row in scrapers.caledonia.main():
    #    save_row(row, table_name='music')

    #for row in scrapers.kazimier.main():
    #    save_row(row, table_name='music')

    update_status()


def save_row(row, table_name='events'):
    scraperwiki.sqlite.save(
        unique_keys=UNIQUE_KEYS,
        data=row,
        table_name=table_name)


def update_status():
    status_text = 'Latest entry: {}'.format(
        get_most_recent_record('events', 'date'))
    print(status_text)

    scraperwiki.status('ok', status_text)


def install_cache():
    requests_cache.install_cache(
        expire_after=(12 * 60 * 60),
        allowable_methods=('GET',))


def download_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return StringIO(response.content)


def get_most_recent_record(table_name, column):
    result = scraperwiki.sql.select(
        "MAX({1}) AS most_recent FROM {0} LIMIT 1".format(table_name, column))
    return result[0]['most_recent']


def process(f):
    """
    Take a file-like object and yield OrderedDicts.
    """
    row = OrderedDict([
        ('date', datetime.datetime.now()),
        ('demo_column_a', True),
        ('demo_column_b', 7.0)])
    yield row

if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    main()
