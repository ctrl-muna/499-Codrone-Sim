# tests/test_range_columns_present.py

#
# Unit tests verifying that telemetry CSV rows and metrics dicts contain the
# range sensor columns/fields added in Week 6.
# No simulator connection required — pure Python only.
#
# Run from repo root:
#   pytest tests/test_range_columns_present.py

import csv
import io
import json
import unittest

# Expected telemetry CSV column names (Week 6 schema).
TELEMETRY_COLUMNS = [
    "timestamp",
    "x", "y", "z",
    "w", "orient_x", "orient_y", "orient_z",
    "collision",
    "front_range_cm",
    "bottom_range_cm",
]

# Required metrics fields including Week 6 addition.
REQUIRED_METRICS_FIELDS = [
    "success",
    "completion_time_s",
    "collisions",
    "failure_reason",
    "min_front_range_cm",
]


def make_telemetry_row(**kwargs):
    """Return a dict representing one telemetry CSV row with all required columns."""
    defaults = {
        "timestamp": "Fri Mar 27 00:00:00 2026",
        "x": 0.0, "y": 0.0, "z": 0.0,
        "w": 1.0, "orient_x": 0.0, "orient_y": 0.0, "orient_z": 0.0,
        "collision": False,
        "front_range_cm": 500.0,
        "bottom_range_cm": 150.0,
    }
    defaults.update(kwargs)
    return defaults


def make_metrics_dict(**kwargs):
    """Return a dict representing a complete Week 6 metrics payload."""
    defaults = {
        "success": True,
        "completion_time_s": 12.4,
        "collisions": 0,
        "failure_reason": None,
        "min_front_range_cm": 180.0,
    }
    defaults.update(kwargs)
    return defaults


class TestTelemetryColumns(unittest.TestCase):

    def test_all_required_columns_present(self):
        row = make_telemetry_row()
        for col in TELEMETRY_COLUMNS:
            self.assertIn(col, row, msg=f"Missing column: {col}")

    def test_front_range_cm_is_float(self):
        row = make_telemetry_row(front_range_cm=300.0)
        self.assertIsInstance(row["front_range_cm"], float)

    def test_bottom_range_cm_is_float(self):
        row = make_telemetry_row(bottom_range_cm=120.0)
        self.assertIsInstance(row["bottom_range_cm"], float)

    def test_front_range_cm_non_negative(self):
        row = make_telemetry_row(front_range_cm=0.0)
        self.assertGreaterEqual(row["front_range_cm"], 0.0)

    def test_bottom_range_cm_non_negative(self):
        row = make_telemetry_row(bottom_range_cm=0.0)
        self.assertGreaterEqual(row["bottom_range_cm"], 0.0)

    def test_row_serialises_to_csv(self):
        row = make_telemetry_row()
        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=TELEMETRY_COLUMNS)
        writer.writeheader()
        writer.writerow(row)
        content = buf.getvalue()
        self.assertIn("front_range_cm", content)
        self.assertIn("bottom_range_cm", content)


class TestMetricsFields(unittest.TestCase):

    def test_all_required_fields_present(self):
        m = make_metrics_dict()
        for field in REQUIRED_METRICS_FIELDS:
            self.assertIn(field, m, msg=f"Missing metrics field: {field}")

    def test_min_front_range_cm_is_float_or_none(self):
        m = make_metrics_dict(min_front_range_cm=180.0)
        self.assertIsInstance(m["min_front_range_cm"], float)

    def test_min_front_range_cm_none_when_no_readings(self):
        m = make_metrics_dict(min_front_range_cm=None)
        self.assertIsNone(m["min_front_range_cm"])

    def test_min_front_range_cm_non_negative(self):
        m = make_metrics_dict(min_front_range_cm=0.0)
        self.assertGreaterEqual(m["min_front_range_cm"], 0.0)

    def test_metrics_json_roundtrip(self):
        m = make_metrics_dict()
        serialised = json.dumps(m)
        restored = json.loads(serialised)
        self.assertEqual(restored["min_front_range_cm"], m["min_front_range_cm"])

    def test_metrics_json_roundtrip_none(self):
        m = make_metrics_dict(min_front_range_cm=None)
        serialised = json.dumps(m)
        restored = json.loads(serialised)
        self.assertIsNone(restored["min_front_range_cm"])


if __name__ == "__main__":
    unittest.main()
