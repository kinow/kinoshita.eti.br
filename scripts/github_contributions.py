#!/usr/bin/env python3

import github
from github import Github
import datetime
from pprint import pprint

"""
Finds all the projects I have ever contributed in GitHub.
Original Perl script:
http://stackoverflow.com/questions/21322778/how-do-i-get-a-list-of-all-the-github-projects-ive-contributed-to-in-the-last-y
"""

# Returns only the 90 last days

USER_NAME="kinow"
FROM=2010
now = datetime.datetime.now()
TO=now.year

URL="https://github.com/%s?tab=contributions&from=%s&to=%s"

def main():
    # First create a Github instance:
    g = Github()
    #github.enable_console_debug_logging()

    projects = set()

    # Then play with your Github objects:
    for event in g.get_user(login='kinow').get_events():
        projects.add(event.repo.name)        

    pprint(projects)

if __name__ == '__main__':
    main()
