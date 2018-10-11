"""
Rohit Suratekar
September 2018

Most of the cast and crew names are not tagged with gender.
We can get this information roughly by checking first name against the gender
API of https://genderize.io/ website. They are very generous to provide 1000
free requests per day.

This will be crud detection but good enough to build a statistics and use it in
our ML models.
"""
import json
import os
import random
import urllib.error
import urllib.request
from collections import Counter
from time import sleep
from helper import *

# Add following if on proxy
# proxy = 'http://proxy.ncbs.res.in:3128'
# os.environ['https_proxy'] = proxy
# os.environ['http_proxy'] = proxy

OUTPUT_FILE = "genders.txt"


def check_name(name):
    """
    Uses 'https://genderize.io/' to get gender of person from first name.
    Information retrieved from this will be saved to OUTPUT_FILE.

    API has limit on 1000 requests per day, you might want to retrieve on
    different days or use VPN
    :param name: Name to be checked
    """
    try:
        contents = urllib.request.urlopen(
            "https://api.genderize.io/?name=%s" % name).read()

        data = json.loads(contents)
        if data['gender'] is not None:
            with open(OUTPUT_FILE, "a") as f:
                print(json.dumps(data), file=f)
    except Exception as e:
        # Keep it broad so that it can catch many unknown errors
        print(str(e))
        pass


def get_retrieved_names():
    """
    This will save bandwidth and API requests
    :return: already downloaded names
    """
    names = []
    try:
        with open(OUTPUT_FILE) as f:
            for line in f:
                data = json.loads(line.strip())
                names.append(data['name'])
    except FileNotFoundError:
        pass
    return names


def get_names():
    """
    Names which we should request from API

    This will also removes names which we have already requested from the API
    to avoid extra requests and save bandwidth

    :return: list of names which we should retrieve from API
    """
    c = Counter()
    g = []
    person = defaultdict(list)
    for cr in get_credits().values():
        for i in cr.cast:
            c.update({i.id})
            person[i.id].append(i)
        for i in cr.crew:
            c.update({i.id})
            person[i.id].append(i)

    # There can be few names which might be used in both genders however we can
    # use any one of them and which should be averaged out at the end
    known_genders = {}

    for i in c.most_common():
        if person[i[0]][0].gender == 0:
            # Take only first name
            if len(person[i[0]][0].name.split(" ")[0].strip()) > 0:
                g.append(person[i[0]][0].name.split(" ")[0].strip())
        else:
            known_genders[person[i[0]][0].name.split(" ")[0].strip()] = \
                person[i[0]][0].gender

    # Removes names for which we already know the gender
    final_names = []
    downloaded_names = get_retrieved_names()
    for name in g:
        try:
            known_genders[name]
        except KeyError:
            if name not in downloaded_names:
                final_names.append(name)
            else:
                pass

    return set(final_names)


def download_all():
    """
    Download missing names and associated gender information
    """
    c = 0
    for name in get_names():
        c += 1
        check_name(name)
        print("downloaded %d" % c)

        # To Avoid spam randomly provide delay between 0 and 1 second
        sleep(random.uniform(0, 0.5))


def run():
    download_all()
