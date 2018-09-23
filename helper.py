"""
Helper methods to extract and arrange data from files to use in further analysis
"""

import csv
from collections import defaultdict

from models import Credits, Movie

MOVIE_FILE = "tmdb_5000_movies.csv"
CREDIT_FILE = "tmdb_5000_credits.csv"


def get_credits() -> dict:
    """
    Extracts all credits including cast and crew
    :return: dictionary of credit object
    """
    all_list = {}
    with open(CREDIT_FILE) as f:
        data = csv.reader(f)
        next(data, None)  # Skip Header
        for line in data:
            c = Credits(line)
            all_list[c.movie_id] = c
    return all_list


def get_movies() -> list:
    """
    Extracts all movies WITHOUT credits.
    Useful for only movie properties analysis
    :return: list of movie objects without credits
    """
    all_list = []
    with open(MOVIE_FILE) as f:
        data = csv.reader(f)
        next(data, None)  # Skip Header
        for line in data:
            all_list.append(Movie(line))
    return all_list


def get_movies_with_credits() -> list:
    """
    Extracts all movies WITH credits.
    Useful for detailed movie analysis
    :return: list of movie objects with credits
    """
    credit_data = get_credits()
    all_list = []
    with open(MOVIE_FILE) as f:
        data = csv.reader(f)
        next(data, None)  # Skip Header
        for line in data:
            m = Movie(line)
            m.credits = credit_data.get(m.id)
            all_list.append(m)
    return all_list


def get_all_people() -> list:
    """
    Arranges all the people with their contribution
    :return:
    """
    crew_data = defaultdict(list)
    cast_data = defaultdict(list)
    for credit in get_credits().values():
        for cast in credit.cast:
            cast_data[cast.id].append(cast)

        for crew in credit.crew:
            crew_data[crew.id].append(crew)

    return [cast_data, crew_data]
