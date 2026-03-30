# tests/test_range_timeout_conversion.py

#
# Unit tests for range sensor timeout logic and unit conversion.
# No simulator connection required — pure Python math only.
#
# Run from repo root:
#   pytest tests/test_range_timeout_conversion.py

import unittest


def metres_to_cm(metres):
    """Convert a distance in metres to centimetres."""
    return metres * 100.0


def cm_to_metres(cm):
    """Convert a distance in centimetres to metres."""
    return cm / 100.0


def is_within_threshold(distance_m, threshold_m):
    """Return True if distance_m is at or below the stop threshold."""
    if distance_m is None:
        return False
    return distance_m <= threshold_m


def polls_within_timeout(timeout_s, interval_s):
    """
    Return the number of sensor polls that fit within timeout_s given
    an interval of interval_s seconds between polls.
    """
    if interval_s <= 0:
        raise ValueError("interval_s must be positive")
    return int(timeout_s / interval_s)


class TestUnitConversion(unittest.TestCase):

    def test_metres_to_cm_basic(self):
        self.assertAlmostEqual(metres_to_cm(1.0), 100.0)

    def test_metres_to_cm_fraction(self):
        self.assertAlmostEqual(metres_to_cm(0.5), 50.0)

    def test_metres_to_cm_zero(self):
        self.assertAlmostEqual(metres_to_cm(0.0), 0.0)

    def test_metres_to_cm_large(self):
        self.assertAlmostEqual(metres_to_cm(50.0), 5000.0)

    def test_cm_to_metres_basic(self):
        self.assertAlmostEqual(cm_to_metres(100.0), 1.0)

    def test_cm_to_metres_fraction(self):
        self.assertAlmostEqual(cm_to_metres(50.0), 0.5)

    def test_roundtrip_metres_cm(self):
        original = 3.75
        self.assertAlmostEqual(cm_to_metres(metres_to_cm(original)), original)


class TestThresholdCheck(unittest.TestCase):

    def test_below_threshold_triggers(self):
        self.assertTrue(is_within_threshold(1.5, 2.0))

    def test_at_threshold_triggers(self):
        self.assertTrue(is_within_threshold(2.0, 2.0))

    def test_above_threshold_does_not_trigger(self):
        self.assertFalse(is_within_threshold(3.0, 2.0))

    def test_none_reading_does_not_trigger(self):
        self.assertFalse(is_within_threshold(None, 2.0))

    def test_zero_distance_triggers(self):
        self.assertTrue(is_within_threshold(0.0, 2.0))


class TestPollCount(unittest.TestCase):

    def test_ten_polls_in_five_seconds(self):
        self.assertEqual(polls_within_timeout(5.0, 0.5), 10)

    def test_one_second_half_interval(self):
        self.assertEqual(polls_within_timeout(1.0, 0.5), 2)

    def test_timeout_shorter_than_interval(self):
        self.assertEqual(polls_within_timeout(0.3, 0.5), 0)

    def test_zero_interval_raises(self):
        with self.assertRaises(ValueError):
            polls_within_timeout(5.0, 0)

    def test_negative_interval_raises(self):
        with self.assertRaises(ValueError):
            polls_within_timeout(5.0, -1)


if __name__ == "__main__":
    unittest.main()
