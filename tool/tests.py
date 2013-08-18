#!/usr/bin/env python
# encoding: utf-8

import unittest
from nose.tools import assert_equal, assert_true, assert_false
from os.path import join, dirname, abspath
import datetime

from scrapers import caledonia
from scrapers import leaf
from scrapers import stgeorgeshall
from scrapers import fact
from scrapers import kazimier
from scrapers import ljmu

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

    def test_urls(self):
        assert_equal(
            set(['http://www.thecaledonialiverpool.com/whats-on/']),
            set([x['url'] for x in self.rows]))


class StGeorgesHallTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(join(SAMPLE_DIR, 'stgeorgeshall.html'), 'r') as f:
            cls.rows = list(stgeorgeshall.process(f))

    def test_correct_number_of_events(self):
        assert_equal(7, len(self.rows))

    def test_venue_always_st_georges_hall(self):
        assert_equal(
            set(["St George's Hall"]),
            set([x['venue'] for x in self.rows]))

    def test_all_dates_are_datetime_dates(self):
        dates = [row['date'] for row in self.rows]
        assert_true(
            all([isinstance(date, datetime.date) for date in dates]))

    def test_the_headlines_are_correct(self):
        assert_equal(
            [
                'The Charlatans',
                'In conversation with Lynda La Plante',
            ],
            [row['headline'] for row in self.rows[0:2]])

        assert_equal(
            [
                "Murder at St George's Hall",
                'Llyr Williams - piano'
            ],
            [row['headline'] for row in self.rows[-2:]])

    def test_urls(self):
        urls = [x['url'] for x in self.rows]
        assert_equal(
            'http://www.stgeorgesliverpool.co.uk/whatson/details.asp'
            '?id=226947',
            urls[0])


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

    def test_urls(self):
        assert_equal(
            set(['http://www.thisisleaf.co.uk/#/on-bold-street/events/']),
            set([x['url'] for x in self.rows]))


class FactScraperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(join(SAMPLE_DIR, 'fact_listings.html'), 'r') as f:
            cls.rows = list(fact.get_all_listings(f))

    def test_correct_number_of_events(self):
        assert_equal(114, len(self.rows))

    def test_venue_always_fact(self):
        assert_equal(
            set(['FACT']),
            set([x['venue'] for x in self.rows]))

    def test_all_dates_are_datetime_dates(self):
        dates = [row['date'] for row in self.rows]
        assert_true(
            all([isinstance(date, datetime.date) for date in dates]))

    def test_date_range_as_expected(self):
        """
        Check that dates without a year are being filled in correctly as next
        year rather than this year.
        """
        dates = [row['date'] for row in self.rows]
        assert_equal(datetime.date(2013, 8, 17), min(dates))
        assert_equal(datetime.date(2014, 6, 24), max(dates))

    def test_the_headlines_are_correct(self):
        assert_equal([
            u'Alan Partridge: Alpha Papa (1)',
            u"The World's End"
        ],
            [row['headline'] for row in self.rows[0:2]])

        assert_equal([
            u'Met. Encore: La Cenerentola',
            u'ROH. Live: Manon Lescaut'
        ],
            [row['headline'] for row in self.rows[-2:]])

    def test_repeated_event_identified(self):
        with open(join(SAMPLE_DIR, 'fact_repeated.html'), 'r') as f:
            assert_false(fact.is_single_event(f))

    def test_exhibition_date_range_event_identified(self):
        with open(join(SAMPLE_DIR, 'fact_exhib.html'), 'r') as f:
            assert_false(fact.is_single_event(f))

    def test_single_event_identified(self):
        with open(join(SAMPLE_DIR, 'fact_single.html'), 'r') as f:
            assert_true(fact.is_single_event(f))

    def test_child_event_identified(self):
        with open(join(SAMPLE_DIR, 'fact_child_event.html'), 'r') as f:
            assert_true(fact.is_child_event(f))

    def test_non_child_event_identified(self):
        with open(join(SAMPLE_DIR, 'fact_single.html'), 'r') as f:
            assert_false(fact.is_child_event(f))


class KazimierScraperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(join(SAMPLE_DIR, 'kazimier_listings.html'), 'r') as f:
            cls.rows = list(kazimier.process(f))

    def test_correct_number_of_events(self):
        assert_equal(27, len(self.rows))

    def test_venue_always_fact(self):
        assert_equal(
            set(['Kazimier']),
            set([x['venue'] for x in self.rows]))

    def test_all_dates_are_datetime_dates(self):
        dates = [row['date'] for row in self.rows]
        assert_true(
            all([isinstance(date, datetime.date) for date in dates]))

    def test_date_range_as_expected(self):
        """
        Check that dates without a year are being filled in correctly as next
        year rather than this year.
        """
        dates = [row['date'] for row in self.rows]
        assert_equal(datetime.date(2013, 8, 21), min(dates))
        assert_equal(datetime.date(2013, 12, 7), max(dates))

    def test_the_headlines_are_correct(self):
        assert_equal([
            u'Manifold - A living exhibition',
            u'Othello'
        ],
            [row['headline'] for row in self.rows[0:2]])

        assert_equal([
            u'Jonathan Wilson',
            u'John Smith'
        ],
            [row['headline'] for row in self.rows[-2:]])

    def test_urls(self):
        urls = [x['url'] for x in self.rows]
        assert_equal(
            'http://www.thekazimier.co.uk/listing/00000000175/',
            urls[0])


class LjmuScraperTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(join(SAMPLE_DIR, 'ljmu_listings.html'), 'r') as f:
            cls.rows = list(ljmu.process(f))

    def test_correct_number_of_events(self):
        assert_equal(4, len(self.rows))

    def test_venue(self):
        assert_equal(
            set(['Redmonds Building', 'Liverpool Philharmonic Hall']),
            set([x['venue'] for x in self.rows]))

    def test_organiser(self):
        assert_equal(
            set(['LJMU']),
            set([x['organiser'] for x in self.rows]))

    def test_all_dates_are_datetime_dates(self):
        dates = [row['date'] for row in self.rows]
        assert_true(
            all([isinstance(date, datetime.date) for date in dates]))

    def test_date_range_as_expected(self):
        """
        Check that dates without a year are being filled in correctly as next
        year rather than this year.
        """
        dates = [row['date'] for row in self.rows]
        assert_equal(datetime.date(2013, 9, 5), min(dates))
        assert_equal(datetime.date(2013, 11, 28), max(dates))

    def test_the_headlines_are_correct(self):
        assert_equal([
            u'Astrobiology: The Hunt for Alien Life',
            (u'Roscoe Lecture Series: Mayors and their Cities – the '
             'Challenges and Opportunities')
        ],
            [row['headline'] for row in self.rows[0:2]])

        assert_equal([
            u'Roscoe Lecture Series: ‘Overcoming Disability and Adversity’',
            (u'Roscoe Lecture Series: 1914 – Why Remembering the Great War'
             ' Matters')
        ],
            [row['headline'] for row in self.rows[-2:]])

    def test_urls(self):
        urls = [x['url'] for x in self.rows]
        assert_equal(
            'http://ljmuastrobiologypubliclecture.eventbrite.co.uk/',
            urls[0])
