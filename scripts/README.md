# Scripts

Random scripts used to generate CV, download data from GitHub, MovieLens, Reddit, etc.

## download_movielens_movies.py

Downloads movies from MovieLens.org website. Creates a movies.json dataset file in the current directory.

One can quickly create a Markdown list of the movies, in alphabetical order, with the following command.

`cat movies.json | jq '.' | sed -r 's/^\s+\"(.*)\",?$/* \1/p' | sed -e '1d' -e '$d'`
