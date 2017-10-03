# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 17:04:59 2017

@author: Mauro
"""

# language tag class

import re

main_folder = "./src/language_support/languages_flags/"
#main_folder = "./languages_flags/"

print("read country-flag table")
with open(main_folder + "country_flags.txt", encoding= "utf-8") as f:
    lines = f.readlines()


country_flag = {}

lines = lines[1:]
while lines:
    tag = lines.pop(0).strip().lower()
    flag_emoji = lines.pop(0).strip()
    ll = re.split("\t| ",lines.pop(0))
    unicode_str = ll[0][2:] + ll[1][2:]
    long_name = " ".join(ll[2:]).strip()

    country_flag[long_name] = flag_emoji


print("read country-languages table")
with open(main_folder + "country_language.txt", errors="ignore") as f:
    lines = f.readlines()

languages_country = []

while lines:

    l = lines.pop(0)

    cl = l.strip().split("\t")


    country = cl[0].strip()
    languages = cl[1].strip().split(",")
    languages = [l.strip() for l in languages]

    languages_country.append((languages,country))


print("read tag language table")
with open(main_folder + "languagetag_language.txt", errors="ignore") as f:
    lines = f.readlines()


dtag_lang = {}

while lines:
    l = lines.pop(0).strip()

    cl = l.split("\t")

    if len(cl) >= 2:
        tag = cl[1].strip()
        if tag:
            language = cl[2].strip()
            language = language.split(";")
            language = language[0]

            dtag_lang[tag] = language


print("read population country table")
with open(main_folder + "country_population.txt", errors="ignore") as f:
    lines = f.readlines()


country_pop = {}

while lines:
    l = lines.pop(0).strip()

    cl = l.split("\t")

    position = cl[0].strip()

    is_valid = True
    for char in position:
        if char not in "0123456789":
            is_valid = False

    if is_valid:

        country = cl[1].strip()

        country = country.split("[")[0]

        pop = int(cl[2].strip().replace(",", ""))

        country_pop[country] = pop


def get_language_flag(tag):
    # find the english long name for the language

    long_name = dtag_lang[tag]


    # find all the countries where italian is spoken

    countries = []
    for languages, country in languages_country:

        is_spoken = False
        for language in languages:
            if long_name in language:
                is_spoken = True
                break

        if is_spoken:
            countries.append(country)


    flags_pop = []
    for country in countries:
        if country in country_flag and country in country_pop:
            flag = country_flag[country]
            pop = country_pop[country]

        pair = (flag, pop, country)
        flags_pop.append(pair)


    flags_pop = sorted(flags_pop, key= lambda x: x[1], reverse=True)


    flags = [flag for flag, _, _ in flags_pop]


    return long_name + " " + "|".join(flags)

