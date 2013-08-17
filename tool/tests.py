#!/usr/bin/env python

import unittest
from nose.tools import assert_equal, assert_true
from os.path import join, dirname, abspath
import datetime

from scrapers import caledonia

SAMPLE_DIR = join(dirname(abspath(__file__)), 'sample_data')


class CaledoniaScraperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(join(SAMPLE_DIR, 'caledonia.html'), 'r') as f:
            cls.rows = list(caledonia.process(f))

    def test_correct_number_of_events(self):
        assert_equal(8, len(self.rows))

    def test_venue_always_the_caledonia(self):
        assert_equal(
            set(['The Caledonia']),
            set([x['venue'] for x in self.rows]))

    def test_all_dates_are_datetime_dates(self):
        dates = [row['date'] for row in self.rows]
        assert_true(
            all([isinstance(date, datetime.date) for date in dates]))

    def test_the_headlines_are_correct(self):
        assert_equal([
            'Loose Moose String Band',
            'Cajun Session',
            'Buffalo Clover (from Nashville, Tennessee)',
            'Downtown Dixieland Band',
            'The Martin Smith Quartet',
            'Loose Moose String Band',
            'The Manouchetones',
            'Marley Chingus'],
            [row['headline'] for row in self.rows])
