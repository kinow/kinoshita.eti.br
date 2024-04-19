---
title: "Coverage report for a GitHub private repository with GitHub Actions"
date: 2023-05-29T20:36:52+03:00
categories:
  - opensource
  - programming
tags:
  - opensource
  - programming
  - coverage
  - software quality
  - github
  - github actions
  - python
images:
  - '/assets/posts/2023-05-29-coverage-report-for-a-github-private-repository-with-github-actions/coverage.png'
---

Normally when you add test coverage to a GitHub repository, the reporting part
boils down to a simple call to some API that will post to a third-party external
service like Coveralls or Codecov. Many are already on the GitHub Actions
Market Place and a few lines of YAML are enough.

{{< showimage image="coverage.png" caption="A Codecov coverage report" class="feature" >}}

We had to report the test coverage of a private GitHub repository of a project
I am working on at the moment, that could not have integration with other services
besides GitHub. So no Coveralls and no Codecov.

Our initial solution was to run the unit tests with coverage (using `pytest` and `pytest-cov`)
using GitHub Actions, like we were already doing, create an XML coverage with
`pytest-cov`, which is compatible with Cobertura's XML. This XML file was used
by [pycobertura](https://github.com/aconrad/pycobertura), a Python utility that
reads Cobertura XML and produces HTML or Markdown report.

Then, using GitHub REST API and the GitHub Actions client, a job in our GitHub actions
pipeline posts the coverage report as a Markdown comment to the current pull request.

But later we realized that `pycobertura` is not able to parse [branch coverage](
https://github.com/aconrad/pycobertura/issues/167). It only works with line
coverage.

The final solution was then to use `pytest-cov` and produce its HTML output,
use [`htmlq`](https://github.com/mgdm/htmlq) to extract the HTML coverage table,
convert it to Markdown with [Pandoc](https://github.com/jgm/pandoc/), and
then post the result as the new Markdown comment to the pull requests.

{{<highlight yaml "lineNos=true,lineNumbersInTable=true,anchorLineNos=true">}}
# File: .github/workflows/ci.yml
name: project demo
on:
  push:
  pull_request:
  workflow_dispatch:
    
permissions:
  content: read

jobs:
  demo_test:
    env:
      COVERAGE_ENABLED: true
    runs-on: ubuntu-latest
    permissions:
      contents: read
      issues: write
      pull-requests: write
    steps:
      - uses: actions/checkout@v3
      - uses: mamba-org/provision-with-micromamba@v15
        with:
          environment-file: environment.yml  # includes pandoc
          cache-download: true
          channels: conda-forge
      - name: Install htmlq
        if: ${{ env.COVERAGE_ENABLED }}
        uses: baptiste0928/cargo-install@v2
        with:
          crate: htmlq
          cache-key: cargo-coverage
      - run: cargo install htmlq
        if: ${{ env.COVERAGE_ENABLED }}
      - run: |
          # Produce the HTML report.
          pytest --cov=demo --cov-report=html --cov-report=xml --cov-branch -m "demo"

          if [[ ${COVERAGE_ENABLED} ]]; then
            # Extract the top header of the pytest HTML report.
            # Passes the HTML through htmlq, extracting the first H1 displayed.
            # Uses tr to delete breaklines and squeeze-repeats blank spaces,
            # saving space - this is used for an HTTP REST request to GitHub API.
            COV_HEADER=$(cat htmlcov/index.html | htmlq --pretty 'header > div > h1:first-of-type' | tr -d '\n' | tr -s ' ')
          
            # Extract the table of the pytest HTML report.
            # Passes the HTML through htmlq, extracting the table element.
            # Uses tr to delete breaklines and squeeze-repeats blank spaces.
            # Then calls sed with an expression that replaces the HTML a
            # elements by only its text.
            COV_TABLE=$(cat htmlcov/index.html | htmlq --pretty 'table' | tr -d '\n' | tr -s ' ' | sed 's|<a[^>]*>\([^<]*\)</a>|\1|g')
          
            # Produce a simplified HTML report.
            echo "${COV_HEADER}${COV_TABLE}" > coverage.html
          
            # Now simply use pandoc to convert HTML to Markdown.
            pandoc --from html --to 'markdown_strict+pipe_tables' coverage.html -o coverage.md
          fi
      - name: Public coverage (stdout)
        # Publish the coverage reports in only one matrix job run.
        # Only run if **NOT** running in a pull request (see step below).
        if: ${{ github.event_name != 'pull_request' && env.COVERAGE_ENABLED }}
        run: |
          cat coverage.md
      - name: Publish coverage reports (bot)
        # Only run if running in a pull request.
        # See for more: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-using-contexts
        if: ${{ github.event_name == 'pull_request' && env.COVERAGE_ENABLED }}
        # Comment on an issue or pull request using GH Actions tooling:
        # https://github.com/actions/github-script#comment-on-an-issue
        uses: actions/github-script@v6
        id: coverage-report
        with:
          github-token: ${{secrets.GITHUB_TOKEN}}
          # Based on: https://github.com/actions/github-script/blob/060d68304cc19ea84d828af10e34b9c6ca7bdb31/.github/workflows/pull-request-test.yml
          script: |
            // Get the existing comments.
            const {data: comments} = await github.rest.issues.listComments({
              owner: context.repo.owner,
              repo: context.repo.repo,
              issue_number: context.payload.number,
            })
            
            // Find any comment already made by the bot.
            const botComment = comments.find(comment => comment.user.id === 41898282)
            const fs = require("fs").promises
            const commentBody = await fs.readFile("coverage.md", "utf8")
            
            if (botComment) {
              console.log(`Updating comment in ${context.repo.owner}/${context.repo.repo}, comment ID: ${botComment.id}`)
              await github.rest.issues.updateComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                comment_id: botComment.id,
                body: commentBody
              })
            } else {
              console.log(`Creating comment in ${context.repo.owner}/${context.repo.repo}`)
              await github.rest.issues.createComment({
                owner: context.repo.owner,
                repo: context.repo.repo,
                issue_number: context.issue.number,
                body: commentBody
              })
            }
{{< / highlight >}}

Now the GitHub bot will write a comment to your current pull request with the
Markdown you produced with `htmlq` and some Shell script. If you update the
pull request, the bot will re-use the existing comment, updating it, which is
convenient as GitHub UI gives you a nice diff for your coverage reports.
