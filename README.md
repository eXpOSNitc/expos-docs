# eXpOS NITC Website
[![Build](https://github.com/ghoshishan/expos-v2/workflows/ci/badge.svg)](https://github.com/ghoshishan/expos-v2/actions)

A modern and feature rich version of [eXpOS NITC](https://exposnitc.github.io/) built using [mkDocs Material](https://squidfunk.github.io/mkdocs-material/).

## Setting Up
### Using Docker
```sh
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```
### Using [`pipenv`](https://pypi.org/project/pipenv/)
```bash
# Clone the repository
$ git clone https://github.com/ghoshishan/expos-v2.git
# Install the packages
$ pipenv install
# Open a virtual env shell
$ pipenv shell

# exit shell
$ exit
```

### Others
```bash
$ pip install -r requirements.txt
```

## Running an instance
```bash
$ mkdocs serve
```
Your version of the website should be up in `http://localhost:8000/`.

## Troubleshooting
Sometimes changes are not reflected on the website, make sure to disable caching in your browser.

## CONTRIBUTING
Please port pages from [https://exposnitc.github.io/](https://exposnitc.github.io/) to Markdown and send a pull request.

The directory structure of the project is available here: [https://github.com/eXpOSNitc/eXpOSNitc.github.io](https://github.com/eXpOSNitc/eXpOSNitc.github.io)
