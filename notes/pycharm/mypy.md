# Using mypy in PyCharm

PyCharm has its own type analysing tool. The existing mypy plugin is broken, and not even
compatible with the latest versions of PyCharm for a couple of years at least.

<img width="1071" height="802" alt="image" src="https://github.com/user-attachments/assets/fde9646b-be67-40d6-9c1f-97624743e86a" />

You can add an external tool in PyCharm to call mypy for the current file.
Just add the Program as the location of `mypy` executable, Arguments set to
any arguments you may want to pass to mypy followed by `$FilePath`, e.g.
`--check-untyped-defs $FilePath$`, and the Working directory set to `$ProjectFileDir$`.
