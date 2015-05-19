# coding: utf-8

import unittest
from decimal import Decimal
from class_tracker.tracker import tracker_exception, TrackerException


@tracker_exception('decimal.Decimal')
def class_tracker_decimal_success():
    a = 1  # NOQA
    b = 2  # NOQA


@tracker_exception('decimal.Decimal')
def class_tracker_decimal_error():
    a = 1  # NOQA
    b = 2  # NOQA
    d = Decimal('4')  # NOQA


class TestClassTracker(unittest.TestCase):

    def test_decimal_success(self):
        class_tracker_decimal_success()

    def test_decimal_error(self):
        with self.assertRaises(TrackerException):
            class_tracker_decimal_error()


if __name__ == '__main__':
    unittest.main(verbosity=2)
