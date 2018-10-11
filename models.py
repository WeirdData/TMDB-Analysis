"""
All models related to database will go here!
"""
import datetime
import json


class PairObject:
    """
    Simple object to hold paired objects
    """

    def __init__(self, data):
        self.data = data
        self.is_special = False
        self.special_label = ''
        try:
            self.id = data['id']
        except KeyError:
            self.is_special = True
            try:
                self.id = data['iso_3166_1']
                self.special_label = 'iso_3166_1'
            except KeyError:
                self.id = data['iso_639_1']
                self.special_label = 'iso_639_1'
        self.name = data['name']


class Movie:
    """
    Movie object to hold all information related to movie
    """

    def __init__(self, data):
        self.data = data
        self.budget = data[0]
        self.genres = []
        for values in json.loads(data[1].strip()):
            self.genres.append(PairObject(values))

        self.homepage = data[2]
        self.id = data[3]
        self.keywords = []
        for values in json.loads(data[4].strip()):
            self.keywords.append(PairObject(values))
        self.original_language = data[5]
        self.original_title = data[6]
        self.overview = data[7]
        self.popularity = float(data[8])
        self.production_companies = []
        for values in json.loads(data[9].strip()):
            self.production_companies.append(PairObject(values))

        self.production_countries = []
        for values in json.loads(data[10].strip()):
            self.production_countries.append(PairObject(values))

        try:
            self.release_date = datetime.datetime.strptime(data[11], "%Y-%m-%d")
        except ValueError:
            self.release_date = datetime.datetime.strptime("3030-01-01",
                                                           "%Y-%m-%d")

        self.revenue = data[12]
        self.runtime = data[13]
        self.spoken_languages = []
        for values in json.loads(data[14].strip()):
            self.spoken_languages.append(PairObject(values))

        self.status = data[15]
        self.tagline = data[16]
        self.title = data[17]
        self.vote_average = float(data[18])
        self.vote_count = float(data[19])
        self.score = self.vote_count * self.vote_average
        self.credits = None


class Cast:
    """
    Cast associated with movie
    """

    def __init__(self, data):
        self.data = data
        self.credit_id = data['credit_id']
        self.gender = data['gender']
        self.id = data['id']
        self.name = data['name']
        self.cast_id = data['cast_id']
        self.character = data['character']
        self.order = data['order']


class Crew:
    """
    Crew associated with movie
    """

    def __init__(self, data):
        self.data = data
        self.credit_id = data['credit_id']
        self.gender = data['gender']
        self.id = data['id']
        self.name = data['name']
        self.department = data['department']
        self.job = data['job']


class Credits:
    """
    This is generalized object to combine cast and crew
    """

    def __init__(self, data):
        self.data = data
        self.movie_id = data[0]
        self.title = data[1]
        self.cast = []

        for values in json.loads(data[2]):
            self.cast.append(Cast(values))

        self.crew = []
        for values in json.loads(data[3]):
            self.crew.append(Crew(values))
