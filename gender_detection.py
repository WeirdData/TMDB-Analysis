import json
import os
import urllib.error
import urllib.request
from collections import Counter
from time import sleep

from helper import *

proxy = 'http://proxy.ncbs.res.in:3128'
os.environ['https_proxy'] = proxy
os.environ['http_proxy'] = proxy

OUTPUT_FILE = "genders.txt"


def check_name(name):
    try:
        contents = urllib.request.urlopen(
            "https://api.genderize.io/?name=%s" % name).read()

        data = json.loads(contents)
        if data['gender'] is not None:
            with open(OUTPUT_FILE, "a") as f:
                print(json.dumps(data), file=f)
    except urllib.error.HTTPError:
        pass


def get_retrieved_names():
    """
    This will save bandwidth and API requests
    :return: already downloaded names
    """
    names = []
    with open(OUTPUT_FILE) as f:
        for line in f:
            data = json.loads(line.strip())
            names.append(data['name'])
    return names


def get_names():
    """
    Names which we should request from API
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
    c = 0
    for name in get_names():
        c += 1
        check_name(name)
        print("downloaded %d" % c)
        sleep(1)  # To Avoid Spam


def run():
    download_all()
