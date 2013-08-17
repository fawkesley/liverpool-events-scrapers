#!/usr/bin/env python

import unittest
from nose.tools import assert_equal, assert_true
from os.path import join, dirname, abspath
import datetime

from scrapers import caledonia
from scrapers import leaf

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
            'Live Music: Loose Moose String Band',
            'Live Music: Cajun Session',
            'Live Music: Buffalo Clover (from Nashville, Tennessee)',
            'Live Music: Downtown Dixieland Band',
            'Live Music: The Martin Smith Quartet',
            'Live Music: Loose Moose String Band',
            'Live Music: The Manouchetones',
            'Live Music: Marley Chingus'],
            [row['headline'] for row in self.rows])


class LeafScraperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(join(SAMPLE_DIR, 'leaf.html'), 'r') as f:
            cls.rows = list(leaf.process(f))

    def test_correct_number_of_events(self):
        assert_equal(20, len(self.rows))

    def test_venue_always_leaf(self):
        assert_equal(
            set(['LEAF on Bold Street']),
            set([x['venue'] for x in self.rows]))

    def test_all_dates_are_datetime_dates(self):
        dates = [row['date'] for row in self.rows]
        assert_true(
            all([isinstance(date, datetime.date) for date in dates]))

    def test_ambiguous_dates_are_correct(self):
        assert_equal(datetime.date(2013, 7, 3), self.rows[-1]['date'])

    def test_the_headlines_are_correct(self):
        self.maxDiff = None
        assert_equal([
            'Leaf Pudding Club',
            'Retro Sunday',
        ],
        [row['headline'] for row in self.rows[0:2]])

        assert_equal([
            'Tea with an Architect',
            'Spotify Wednesdays'
        ],
        [row['headline'] for row in self.rows[-2:]])
