#!/usr/bin/env python3

import requests
import json
from pprint import pprint as pp
import locale
from functools import cmp_to_key
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

import getpass

USER = os.environ.get("movielens_user")
PASS = os.environ.get("movielens_pass")

if PASS == None or PASS == '':
    PASS = getpass.getpass("Enter password:")

class MovieLens(object):

    def __init__(self):
        self.base_url = 'https://movielens.org/api'
        self.timeout = 30.0 #seconds
        self.headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.5',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/json;charset=utf-8',
            'Host': 'movielens.org',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0'
        }

    def login(self, username, password):
        self.headers['Referer'] = 'https://movielens.org/login'
        url = "%s/%s" % (self.base_url, "sessions")
        payload = {'userName': username, 'password': password}
        r = requests.post(url, data=json.dumps(payload), headers=self.headers, timeout=self.timeout)
        if not r.cookies:
            raise Exception(f"No Cookie set after auth! Response: {r.json()}")
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
            print("Downloading page %d" % (current_page))
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
    print(str(cookies))
    movies = ml.list_all_rated_movies(cookies)
    movies = sorted(movies, key=cmp_to_key(locale.strcoll))  # locale-aware sort order
    movies_html_file = dotenv_path = join(dirname(__file__), '../pages/movies.html')
    header = """---
title: 'Movies'
author: kinow
tags: {  }
date: '2017-04-17'
time: '23:30:33'
---

Feel free to suggest me some good movies that may be missing from my list!

"""
    with open(movies_html_file, 'w+') as outfile:
        outfile.write(header)
        for movie in movies:
            outfile.write("* {}\n".format(movie))

if __name__ == '__main__':
    main()
