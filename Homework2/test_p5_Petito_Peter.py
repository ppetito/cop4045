"""Unit tests for the weather station analyzer functions."""

import datetime
import os
import tempfile
import unittest

from p5_Petito_Peter import (
    read_observations,
    station_outliers,
    station_statistics,
    write_statistics,
)


class WeatherStationAnalyzerTests(unittest.TestCase):
    """Test reading, analyzing, and writing weather-station observations."""

    def setUp(self):
        """Create an isolated temporary directory for each test."""
        self.temporary_directory = tempfile.TemporaryDirectory()

    def tearDown(self):
        """Remove the temporary directory and its test files."""
        self.temporary_directory.cleanup()

    def _write_input_file(self, contents):
        """Create an input file containing the supplied observation text.

        Args:
            contents: Text to write to the temporary input file.

        Returns:
            The path to the created input file.
        """
        path = os.path.join(self.temporary_directory.name, "observations.txt")
        with open(path, "w", encoding="utf-8") as input_file:
            input_file.write(contents)
        return path

    def test_read_observations_multiple_stations_and_negative_temperature(self):
        """Read observations for multiple stations, including a negative value."""
        filename = self._write_input_file(
            "North,09:28:09 AM 04/20/2026,-12.5\n"
            "South,09:29:09 AM 04/20/2026,80.0\n"
            "North,09:27:09 AM 04/20/2026,10.0\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(errors, [])
        self.assertEqual(set(observations), {"North", "South"})
        self.assertEqual(
            observations["North"],
            [
                (datetime.datetime(2026, 4, 20, 9, 27, 9), 10.0),
                (datetime.datetime(2026, 4, 20, 9, 28, 9), -12.5),
            ],
        )

    def test_read_observations_rejects_duplicate_station_date(self):
        """Reject a second observation with the same station and date."""
        filename = self._write_input_file(
            "North,09:28:09 AM 04/20/2026,70.0\n"
            "North,09:28:09 AM 04/20/2026,71.0\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(len(observations["North"]), 1)
        self.assertEqual(errors, [(2, "duplicate station/date observation")])

    def test_read_observations_rejects_out_of_range_temperatures(self):
        """Reject temperatures below -100.0 and above 150.0."""
        filename = self._write_input_file(
            "North,09:28:09 AM 04/20/2026,-100.1\n"
            "South,09:28:09 AM 04/20/2026,150.1\n"
            "Valid,09:28:09 AM 04/20/2026,150.0\n"
        )

        observations, errors = read_observations(filename)

        self.assertEqual(observations, {
            "Valid": [(datetime.datetime(2026, 4, 20, 9, 28, 9), 150.0)]
        })
        self.assertEqual(
            errors,
            [
                (1, "temperature out of valid range"),
                (2, "temperature out of valid range"),
            ],
        )

    def test_station_statistics_calculates_minimum_maximum_and_mean(self):
        """Calculate accurate minimum, maximum, and mean temperatures."""
        date = datetime.datetime(2026, 4, 20, 9, 28, 9)
        observations = {"North": [(date, -10.0), (date, 10.0), (date, 20.0)]}

        self.assertEqual(station_statistics(observations), {
            "North": (-10.0, 20.0, 20.0 / 3.0)
        })

    def test_station_outliers_returns_latest_temperature_above_mean(self):
        """Return only stations whose latest temperature exceeds their mean."""
        earlier = datetime.datetime(2026, 4, 20, 9, 28, 9)
        latest = datetime.datetime(2026, 4, 21, 9, 28, 9)
        observations = {
            "Outlier": [(earlier, 10.0), (latest, 30.0)],
            "Normal": [(earlier, 30.0), (latest, 10.0)],
        }

        self.assertEqual(
            station_outliers(observations),
            {"Outlier": (latest, 30.0, 20.0)},
        )

    def test_write_statistics_orders_stations_and_formats_numbers(self):
        """Write lexicographically sorted stations with one decimal digit."""
        filename = os.path.join(self.temporary_directory.name, "statistics.txt")
        statistics = {
            "Zulu": (-1.0, 2.0, 0.5),
            "Alpha": (1.0, 4.0, 2.5),
        }

        write_statistics(filename, statistics)

        with open(filename, "r", encoding="utf-8") as output_file:
            self.assertEqual(
                output_file.read(),
                "Alpha,1.0,4.0,2.5\nZulu,-1.0,2.0,0.5\n",
            )

    def test_read_observations_reports_missing_input_file(self):
        """Raise a clear FileNotFoundError when the input file is absent."""
        filename = os.path.join(self.temporary_directory.name, "missing.txt")

        with self.assertRaises(FileNotFoundError):
            read_observations(filename)


if __name__ == "__main__":
    unittest.main()
