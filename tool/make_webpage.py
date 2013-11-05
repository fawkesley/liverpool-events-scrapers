#!/usr/bin/env python
# encoding: utf-8

from __future__ import unicode_literals

import logging
import scraperwiki
import datetime
from jinja2 import Template


def main():
    logging.basicConfig(level=logging.DEBUG)
    with open('index.html.template', 'r') as f:
        html = f.read()
        logging.debug(html)
        template = Template(html)

    events = list(get_upcoming_events(days=14))

    with open('index.html', 'w') as f:
        out = template.render(
            events=events,
            title=('Talks, Lectures, Discussion, Workshops in Liverpool | '
                   'Spoken Liverpool'),
            h1='Upcoming Events')
        logging.info(out)
        f.write(out)


def get_upcoming_events(days=14, start=datetime.datetime.now().date()):
    query = (
        'organiser, venue, date, headline, url '
        'FROM events '
        'WHERE date > DATE("{start}") '
        'AND date < DATE("{start}", "+{days} days") '
        'ORDER BY date ASC;'.format(start=start, days=days))
    logging.debug(query)
    result = scraperwiki.sqlite.select(query)
    logging.debug(result)
    for event in result:
        for key, value in event.items():
            logging.info("{}: {}".format(key, value))
        new_event = dict(event)
        new_event['date'] = pretty_date(event['date'])
        yield new_event


def pretty_date(date_string):
    """
    >>> pretty_date('2013-08-20')
    "20 August '13 (Tuesday)"
    """
    assert isinstance(date_string, basestring)

    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')  # parse
    return date.strftime("%d %B '%y (%A)")


if __name__ == '__main__':
    main()
