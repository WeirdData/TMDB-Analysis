from collections import Counter

import numpy as np

from helper import *


def get_keyword_bin(index: int) -> int:
    b = range(0, 6000, 100)
    for i in b:
        if index < i:
            return b.index(i)


def get_input_output():
    movies = get_movies()

    genres = Counter()
    keywords = Counter()
    for movie in movies:
        for k in movie.keywords:
            keywords.update({k.name})
        for g in movie.genres:
            genres.update({g.name})

    keyword_list = []
    genres_keys = []
    for k in genres.most_common():
        genres_keys.append(k[0])
    for k in keywords.most_common():
        if k[1] > 1:
            keyword_list.append(k[0])

    input_genres = None
    input_keywords = None
    output_array = None
    for movie in movies:
        current_genres = [0] * len(genres_keys)
        current_keywords = [0] * (get_keyword_bin(len(keyword_list)) + 2)
        # +2 because additional last column for keywords with only single use

        for g in movie.genres:
            current_genres[genres_keys.index(g.name)] = 1

        for k in movie.keywords:
            try:
                current_keywords[
                    get_keyword_bin(keyword_list.index(k.name))] = 1
            except ValueError:
                current_keywords[-1] = 1

        if input_genres is None:
            input_genres = current_genres
            input_keywords = current_keywords
            output_array = [movie.score]
        else:
            output_array = np.vstack((output_array, [movie.score]))
            input_keywords = np.vstack((input_keywords, current_keywords))
            input_genres = np.vstack((input_genres, current_genres))

    return input_genres.T, input_keywords.T, output_array


def run():
    get_input_output()
