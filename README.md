# kinoshita.eti.br

![GitHub Pages](https://github.com/kinow/kinoshita.eti.br/workflows/GitHub%20Pages/badge.svg)

[**kinoshita.eti.br**](https://kinoshita.eti.br/) personal home page.

## Building

Built with [Ruby](https://www.ruby-lang.org/en/), [Jekyll](https://www.ruby-lang.org/en/),
and some [Python](https://www.python.org/) scripts. Layout based on
[Minima](https://github.com/jekyll/minima) Jekyll theme.

For Linux:

```bash
bundle install
bundle exec jekyll serve -w -i
```

For Windows:

```bash
bundle install
jekyll serve --skip-initial-build -w -i
```

`--skip-initial-build` is necessary to prevent it from copying files when building
for the first time. There are files with special characters (e.g. "São Paulo") that
fail to be accessed with `File.utime`.

## License

Blog and source code licensed under the Commons Creative Attribution 4.0 International (CC BY 4.0).

For the arts contents, please refer to each media license when provided, or get in contact for more information.
