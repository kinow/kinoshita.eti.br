#!/usr/bin/env python3

import json
import locale
import os
from functools import cmp_to_key
from os.path import join, dirname

import requests
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

import getpass

USER = os.environ.get("movielens_user")
PASS = os.environ.get("movielens_pass")

if not PASS:
    PASS = getpass.getpass("Enter password:")

class MovieLens(object):

    def __init__(self):
        self.base_url = 'https://movielens.org/api'
        self.timeout = 30.0 #seconds
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'movielens.org',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0'
        }

    def login(self, username, password):
        if not username or not password:
            raise ValueError("Must provide non-empty credentials")
        headers = self.headers.copy()
        headers['Referer'] = 'https://movielens.org/login'
        url = "%s/%s" % (self.base_url, "sessions")
        payload = {'userName': username, 'password': password}
        r = requests.post(url, data=json.dumps(payload), headers=headers, timeout=self.timeout)
        if not r.cookies:
            raise Exception("No Cookie set after auth! Response: " + str(r.json()))
        return r.cookies

    def explore(self, params, cookies):
        url = "%s/%s" % (self.base_url, "movies/explore")
        r = requests.get(url, params=params, cookies=cookies, headers=self.headers, timeout=self.timeout)
        return r.json()

    def _get_last_page(self, json_data):
        return int(json_data['data']['pager']['totalPages'])

    def _get_movies(self, json_data):
        movies = []
        results = json_data['data']['searchResults']
        for result in results:
            movies.append("%s (%s)" % (result['movie']['title'], result['movie']['releaseYear']))
        return movies

    def list_all_rated_movies(self, cookies):
        movies = []
        current_page = 1

        while True:
            print("Downloading page %d" % current_page)
            resp = self.explore(params={'hasRated': 'yes', 'sortBy': 'userRatedDate', 'page': current_page}, cookies=cookies)
            movies.extend(self._get_movies(resp))
            last_page = self._get_last_page(resp)
            if current_page >= last_page:
                break
            current_page += 1

        return movies

def main():
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    ml = MovieLens()
    cookies = ml.login(USER, PASS)
    movies = ml.list_all_rated_movies(cookies)
    movies = sorted(movies, key=cmp_to_key(locale.strcoll))  # locale-aware sort order
    movies_html_file = join(dirname(__file__), '../_pages/movies.md')
    header = """---
title: 'Movies'
layout: page
permalink: "/movies/"
note: "Some of the movies I have watched so far. Suggestions are welcome."
---

"""
    with open(movies_html_file, 'w+') as outfile:
        outfile.write(header)
        for movie in movies:
            outfile.write("* {}\n".format(movie))

if __name__ == '__main__':
    main()
