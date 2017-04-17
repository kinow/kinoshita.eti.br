#!/usr/bin/env python3

import requests
import json
from pprint import pprint as pp

import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

USER = os.environ.get("movielens_user")
PASS = os.environ.get("movielens_pass")

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
            'DNT': '1',
            'Host': 'movielens.org',
            'Pragma': 'no-cache',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:42.0) Gecko/20100101 Firefox/42.0'
        }

    def login(self, username, password):
        self.headers['Referer'] = 'https://movielens.org/login'
        url = "%s/%s" % (self.base_url, "sessions")
        payload = {'userName': username, 'password': password}
        r = requests.post(url, data=json.dumps(payload), headers=self.headers, timeout=self.timeout)
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
    ml = MovieLens()
    cookies = ml.login(USER, PASS)
    movies = ml.list_all_rated_movies(cookies)
    with open('movies.json', 'w') as outfile:
        json.dump(movies, outfile)
        print("Done!")

if __name__ == '__main__':
    main()
