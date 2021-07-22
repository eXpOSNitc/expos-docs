<div align="center">
    <img src="./docs/assets/favicon.png">
</div>
<h1 align="center">eXpOS NIT-C Website</h1>

<div align="center">
  A modern and feature rich version of <a href="https://exposnitc.github.io">eXpOS NITC</a> built using <a href="https://squidfunk.github.io/mkdocs-material/">mkDocs Material</a>.
</div>

## Setting Up

### Using Docker

```sh
docker run --rm -it -p 8000:8000 -v ${PWD}:/docs squidfunk/mkdocs-material
```

### Using [`pipenv`](https://pypi.org/project/pipenv/)

```bash
# Clone the repository
$ git clone https://github.com/eXpOSNitc/expos-docs.git
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

Your version of the website should be up in [`http://localhost:8000/`](http://localhost:8000/).

## Troubleshooting

Sometimes changes are not reflected on the website, make sure to disable caching in your browser.

## Contributing

If you encounter issues with the website or have fixes please raise a pull request/issue.
