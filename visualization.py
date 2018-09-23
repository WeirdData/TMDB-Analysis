"""
Gender IDs = 0: Not set, 1:Female, 2:Male
"""
import datetime
from collections import Counter

import matplotlib
import matplotlib.pylab as plt
import numpy as np
from SecretColors.palette import Palette, rgb_to_hex, text_color

from helper import *

ibm = Palette()


def general_statistics():
    """
    General statistics about available data-set
    """
    movies = get_movies()
    c = Counter()
    g = Counter()
    d = Counter()
    p = Counter()
    pc = Counter()
    person = defaultdict(list)
    for cr in get_credits().values():
        for i in cr.cast:
            c.update({i.id})
            person[i.id].append(i)
        for i in cr.crew:
            c.update({i.id})
            d.update({i.department})
            person[i.id].append(i)

    for m in movies:
        for i in m.production_companies:
            p.update({i.id})
        for i in m.production_countries:
            pc.update({i.id})

    for i in c.most_common():
        g.update({person[i[0]][0].gender})

    print("Total no of movies : " + str(len(movies)))
    print("Total no of unique people : " + str(len(c)))
    print("Total no of production companies : " + str(len(p)))
    print("Total no of production countries : " + str(len(pc)))
    print("Total no of departments in crew : " + str(len(d)))

    for k in g.most_common():
        if k[0] == 0:
            print("Total no of not_set : " + str(k[1]))
        elif k[0] == 1:
            print("Total no of females : " + str(k[1]))
        else:
            print("Total no of males : " + str(k[1]))


def check_chronology():
    year_counter = []
    month_counter = Counter()
    for m in get_movies():
        year_counter.append(m.release_date.year)
        month_counter.update({m.release_date.strftime("%b")})

    month_name = []
    month_value = []

    for k in month_counter.most_common():
        month_name.append(k[0])
        month_value.append(k[1])

    year_counter.remove(3030)  # This was default year used if information is
    #  not available
    plt.subplot(121)
    plt.hist(year_counter, 100, color="#2d74da")
    plt.xlabel("Year")
    plt.ylabel("Frequency")
    plt.subplot(122)
    plt.bar(range(len(month_value)), list(map(float, month_value)),
            color="#95d13c")
    plt.xticks(range(len(month_name)), month_name)
    plt.xlabel("Month")
    plt.ylabel("Frequency")
    plt.xticks(rotation=90)
    plt.show()


def check_chronology_trend():
    year_difference = 5
    cmap = ibm.cmap_of(matplotlib, color=ibm.orange())
    year_slots = [x for x in range(1900, 2030, year_difference)]
    year_counter = defaultdict(Counter)
    for m in get_movies():
        for k in year_slots:
            if m.release_date.year < k:
                year_counter[k].update({m.release_date.month})
                break

    data_array = defaultdict(list)
    for k in year_counter.keys():
        for i in range(1, 13):
            data_array[k].append(year_counter[k].get(i))

    names = []
    values = []
    year_slots.reverse()
    for y in year_slots:
        if data_array.get(y) is not None:
            names.append(str(y) + "-" + str(y - year_difference))
            values.append(data_array.get(y))

    figure = plt.figure()
    ax = figure.add_subplot(111)

    values = np.asarray(values)
    ind = range(len(names))
    base = np.zeros(len(names))
    for column in range(len(values[0])):
        # I am too lazy to make separate month list so I will make datetime
        # object to get month
        d = datetime.datetime.strptime("2018-%d-1" % (column + 1), "%Y-%m-%d")
        v = np.asarray([x if x is not None else 0 for x in values[:, column]])
        ax.barh(ind, v, left=base, color=cmap(column / len(values[0])),
                label=d.strftime("%b"))
        base += v

    for p in ax.patches:
        width, height = p.get_width(), p.get_height()
        x, y = p.get_xy()
        c = p.get_facecolor()
        if width > 50:
            ax.annotate('{:.0f}'.format(width),
                        (p.get_x() + .15 * width, p.get_y() + .3 * height),
                        color=text_color(rgb_to_hex((c[0], c[1], c[2]))))

    plt.yticks(ind, names)
    plt.legend(loc=0)
    plt.xlabel("Movie Released")
    plt.show()


def test():
    pass


def run():
    general_statistics()
