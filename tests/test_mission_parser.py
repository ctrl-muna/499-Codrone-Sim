# tests/test_mission_parser.py

#
# Tests load_mission() from sdk/client/mission_runner.py.
# No simulator connection required — pure JSON parsing logic only.
#
# Run from repo root:
#   pytest tests/test_mission_parser.py

import json
import os
import sys
import tempfile
import unittest

# Add sdk/client to path so mission_runner can be imported without installation.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "sdk", "client"))

from mission_runner import load_mission, VALID_COMMANDS  # noqa: E402


class TestMissionParser(unittest.TestCase):

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _write_temp_mission(self, data):
        """Write a mission dict to a temp JSON file and return the path."""
        f = tempfile.NamedTemporaryFile(
            mode="w", suffix=".json", delete=False
        )
        json.dump(data, f)
        f.close()
        return f.name

    def _square_path(self):
        """Return the absolute path to missions/square_path.json."""
        return os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "missions", "square_path.json")
        )

    # ------------------------------------------------------------------
    # square_path.json baseline tests
    # ------------------------------------------------------------------

    def test_square_path_loads(self):
        """square_path.json loads without error and returns a list."""
        steps = load_mission(self._square_path())
        self.assertIsInstance(steps, list)

    def test_square_path_is_non_empty(self):
        """square_path.json has at least one step."""
        steps = load_mission(self._square_path())
        self.assertGreater(len(steps), 0)

    def test_each_step_has_command_and_duration(self):
        """Every step in square_path.json has 'command' and 'duration' keys."""
        steps = load_mission(self._square_path())
        for i, step in enumerate(steps):
            self.assertIn("command", step, msg=f"Step {i} missing 'command'")
            self.assertIn("duration", step, msg=f"Step {i} missing 'duration'")

    def test_all_commands_are_valid(self):
        """Every command in square_path.json is in VALID_COMMANDS."""
        steps = load_mission(self._square_path())
        for step in steps:
            self.assertIn(step["command"], VALID_COMMANDS)

    def test_all_durations_are_non_negative(self):
        """Every duration in square_path.json is >= 0."""
        steps = load_mission(self._square_path())
        for i, step in enumerate(steps):
            self.assertGreaterEqual(
                step["duration"], 0, msg=f"Step {i} has negative duration"
            )

    # ------------------------------------------------------------------
    # Validation error tests
    # ------------------------------------------------------------------

    def test_missing_steps_key_raises(self):
        """A mission file without a 'steps' key raises ValueError."""
        path = self._write_temp_mission({"description": "no steps here"})
        try:
            with self.assertRaises(ValueError):
                load_mission(path)
        finally:
            os.unlink(path)

    def test_empty_steps_raises(self):
        """A mission file with an empty steps list raises ValueError."""
        path = self._write_temp_mission({"steps": []})
        try:
            with self.assertRaises(ValueError):
                load_mission(path)
        finally:
            os.unlink(path)

    def test_unknown_command_raises(self):
        """A step with an unrecognised command name raises ValueError."""
        data = {"steps": [{"command": "Fly_Sideways", "duration": 2}]}
        path = self._write_temp_mission(data)
        try:
            with self.assertRaises(ValueError):
                load_mission(path)
        finally:
            os.unlink(path)

    def test_missing_duration_raises(self):
        """A step missing the 'duration' field raises ValueError."""
        data = {"steps": [{"command": "Takeoff"}]}
        path = self._write_temp_mission(data)
        try:
            with self.assertRaises(ValueError):
                load_mission(path)
        finally:
            os.unlink(path)

    def test_missing_command_raises(self):
        """A step missing the 'command' field raises ValueError."""
        data = {"steps": [{"duration": 2}]}
        path = self._write_temp_mission(data)
        try:
            with self.assertRaises(ValueError):
                load_mission(path)
        finally:
            os.unlink(path)

    def test_negative_duration_raises(self):
        """A step with a negative duration raises ValueError."""
        data = {"steps": [{"command": "Forward", "duration": -1}]}
        path = self._write_temp_mission(data)
        try:
            with self.assertRaises(ValueError):
                load_mission(path)
        finally:
            os.unlink(path)

    def test_file_not_found_raises(self):
        """A path that does not exist raises FileNotFoundError."""
        with self.assertRaises(FileNotFoundError):
            load_mission("/nonexistent/path/missing.json")


if __name__ == "__main__":
    unittest.main()
