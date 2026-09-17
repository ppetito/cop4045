
# Peter Petito - Homework 2
# Problem 5 - Weather Station Analyzer

import datetime
import sys


def read_observations(filename):
    """Read, validate, and organize weather-station observations.

    Args:
        filename: Path to a text file containing one observation per line in
            ``station,date,temperature`` format.

    Returns:
        A tuple containing a dictionary that maps station names to sorted lists
        of ``(date, temperature)`` tuples and a list of ``(line_number,
        error_message)`` tuples for invalid input lines.
    """
    observations = {}
    errors = []
    seen_observations = set()

    with open(filename, "r", encoding="utf-8") as observation_file:
        for line_number, line in enumerate(observation_file, start=1):
            fields = line.rstrip("\n").split(",")
            if len(fields) != 3:
                errors.append((line_number, "expected station,date,temperature"))
                continue

            station, date_text, temperature_text = (field.strip() for field in fields)

            try:
                date = datetime.datetime.strptime(
                    date_text, "%I:%M:%S %p %m/%d/%Y"
                )
            except ValueError:
                errors.append((line_number, "invalid date"))
                continue

            try:
                temperature = float(temperature_text)
            except ValueError:
                errors.append((line_number, "invalid temperature"))
                continue

            if not -100.0 <= temperature <= 150.0:
                errors.append((line_number, "temperature out of valid range"))
                continue

            observation_key = (station, date)
            if observation_key in seen_observations:
                errors.append((line_number, "duplicate station/date observation"))
                continue

            seen_observations.add(observation_key)
            observations.setdefault(station, []).append((date, temperature))

    for station_observations in observations.values():
        station_observations.sort(key=lambda observation: observation[0])

    return observations, errors


def station_statistics(observations):
    """Calculate minimum, maximum, and mean temperatures for each station.

    Args:
        observations: A dictionary mapping station names to lists of
            ``(date, temperature)`` tuples.

    Returns:
        A dictionary mapping each station name to a tuple containing its
        minimum temperature, maximum temperature, and mean temperature.
    """
    statistics = {}

    for station, station_observations in observations.items():
        temperatures = [temperature for _, temperature in station_observations]
        minimum = min(temperatures)
        maximum = max(temperatures)
        mean = sum(temperatures) / len(temperatures)
        statistics[station] = (minimum, maximum, mean)

    return statistics


def station_outliers(observations):
    """Return stations whose latest temperature exceeds their mean temperature.

    Args:
        observations: A dictionary mapping station names to date-sorted lists
            of ``(date, temperature)`` tuples.

    Returns:
        A dictionary mapping each outlying station name to a
        ``(date, temperature, mean)`` tuple for its latest observation.
    """
    statistics = station_statistics(observations)

    return {
        station: (station_observations[-1][0], station_observations[-1][1],
                  statistics[station][2])
        for station, station_observations in observations.items()
        if station_observations[-1][1] > statistics[station][2]
    }


def write_statistics(filename, statistics):
    """Write station temperature statistics to a text file.

    Args:
        filename: Path of the output text file.
        statistics: A dictionary mapping station names to
            ``(minimum, maximum, mean)`` temperature tuples.
    """
    with open(filename, "w", encoding="utf-8") as output_file:
        for station in sorted(statistics):
            minimum, maximum, mean = statistics[station]
            output_file.write(
                f"{station},{minimum:.1f},{maximum:.1f},{mean:.1f}\n"
            )


def main():
    """Read observations, display results, and write station statistics.

    The input filename is read from ``sys.argv[1]`` and the output filename is
    read from ``sys.argv[2]``. The program exits with status code 1 if either
    file cannot be accessed.
    """
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} INPUT_FILENAME OUTPUT_FILENAME")
        sys.exit(1)

    input_filename = sys.argv[1]
    output_filename = sys.argv[2]

    try:
        observations, errors = read_observations(input_filename)
    except FileNotFoundError:
        print(f"Error: input file not found: {input_filename}")
        sys.exit(1)
    except (OSError, UnicodeError) as error:
        print(f"Error: could not read input file '{input_filename}': {error}")
        sys.exit(1)

    for line_number, error_message in errors:
        print(f"Line {line_number}: {error_message}")

    statistics = station_statistics(observations)
    outliers = station_outliers(observations)
    print("Statistics:", statistics)
    print("Outliers:", outliers)

    try:
        write_statistics(output_filename, statistics)
    except FileNotFoundError:
        print(f"Error: output file path not found: {output_filename}")
        sys.exit(1)
    except (OSError, UnicodeError) as error:
        print(f"Error: could not write output file '{output_filename}': {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
