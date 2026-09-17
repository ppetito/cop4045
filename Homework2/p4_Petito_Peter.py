# Peter Petito - Homework 2
# Problem 4

import csv
from typing import Dict, List, Tuple, Optional

CASTS_FIELDS = ['Title', 'Year', 'Director', 'Actor1', 'Actor2', 'Actor3', 'Actor4', 'Actor5']


def load_csv_rows(filename: str, fieldnames: Optional[List[str]] = None) -> List[dict]:
    """Read a CSV file and return its rows as a list of dicts (uses fieldnames if the file has no header)."""
    try:
        with open(filename, 'r', encoding='utf-8', newline='') as f:
            reader = csv.DictReader(f, fieldnames=fieldnames)
            return list(reader)
    except Exception as error:
        print(f"Error reading '{filename}': {error}")
        raise


def load_casts(filename: str) -> Dict[Tuple[str, str], Tuple[str, List[str]]]:
    """Return a dict mapping (title, year) -> (director, [actors]) from a top-casts CSV file (no header)."""
    rows = load_csv_rows(filename, fieldnames=CASTS_FIELDS)
    casts = {}
    for row in rows:
        key = (row['Title'], row['Year'])
        actors = [row[f'Actor{i}'] for i in range(1, 6) if row.get(f'Actor{i}')]
        casts[key] = (row['Director'], actors)
    return casts


def display_ranking(ranking: List[tuple], limit: Optional[int] = None) -> None:
    """Print a ranking list (a list of tuples), optionally cut to the first 'limit' entries."""
    for entry in (ranking[:limit] if limit else ranking):
        print(entry)


def display_top_collaborations(top_rated_file: str, casts_file: str, limit: Optional[int] = None) -> List[Tuple[str, str, int]]:
    """
    Display the ranking of (director, actor, movie_count) for director and actor pairs
    that collaborated on movies in the top-rated list, ordered by descending count.
    """
    try:
        casts = load_casts(casts_file)
        top_rated = load_csv_rows(top_rated_file)

        counts: Dict[Tuple[str, str], int] = {}
        for movie in top_rated:
            key = (movie['Title'], movie['Year'])
            if key in casts:
                director, actors = casts[key]
                for actor in actors:
                    pair = (director, actor)
                    counts[pair] = counts.get(pair, 0) + 1

        ranking = [(director, actor, count) for (director, actor), count in counts.items()]
        ranking.sort(key=lambda entry: entry[2], reverse=True)
        display_ranking(ranking, limit)
        return ranking
    except Exception as error:
        print(f"Error computing top collaborations: {error}")
        raise


def display_top_actors(top_grossing_file: str, casts_file: str, limit: Optional[int] = None) -> List[Tuple[str, int]]:
    """
    Display the ranking of actors from the top-grossing list ordered by the
    total USA box office (descending) of the movies they acted in.
    """
    try:
        casts = load_casts(casts_file)
        top_grossing = load_csv_rows(top_grossing_file)

        totals: Dict[str, int] = {}
        for movie in top_grossing:
            key = (movie['Title'], movie['Year'])
            if key in casts:
                box_office = int(movie['USA Box Office'])
                _, actors = casts[key]
                for actor in actors:
                    totals[actor] = totals.get(actor, 0) + box_office

        ranking = list(totals.items())
        ranking.sort(key=lambda entry: entry[1], reverse=True)
        display_ranking(ranking, limit)
        return ranking
    except Exception as error:
        print(f"Error computing top actors: {error}")
        raise


def main() -> None:
    top_rated_file = 'imdb-top-rated.csv'
    top_grossing_file = 'imdb-top-grossing.csv'
    casts_file = 'imdb-top-casts.csv'

    print("a) Top director/actor collaborations (top 10):")
    display_top_collaborations(top_rated_file, casts_file, limit=10)

    print("\nb) Top actors by total box office (top 10):")
    display_top_actors(top_grossing_file, casts_file, limit=10)


if __name__ == "__main__":
    main()