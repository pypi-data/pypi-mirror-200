# Installation from pip3

```shell
pip3 install --verbose subtitlecore
python -m spacy download en_core_web_trf
python -m spacy download es_dep_news_trf
```

# Usage

Please refer to [api docs](https://qishe-nlp.github.io/subtitlecore/).

### Excutable usage

* Get subtitle content

```shell
subtitlecore_content --srtfile test.srt --lang en
``` 

* Parse srtfile into sentences with timestamp

```shell
subtitlecore_parse2sens --srtfile test.srt --lang en
```

* Parse srtfile into plain text
```shell
subtitlecore_parse2text --srtfile test.srt --lang en
```

### Package usage
```
from subtitlecore import Subtitle

def get_subtitle_content(srtfile, lang):
  st = Subtitle(srtfile, lang)
  for line_info in st.content:
    print(line_info)

def parse2sens(srtfile, lang):
  st = Subtitle(srtfile, lang)
  content_sens = st.sentenize()
  for e in content_sens:
    print(e)

def parse2text(srtfile, lang):
  st = Subtitle(srtfile, lang)
  text = st.plaintext()
  print(text)
```

# Development

### Clone project
```
git clone https://github.com/qishe-nlp/subtitlecore.git
```

### Install [poetry](https://python-poetry.org/docs/)

### Install dependencies
```
poetry update
```

### Test
```
poetry run pytest -rP
```
which run tests under `tests/*`

### Execute
```
poetry run subtitlecore_content --help
poetry run subtitlecore_parse2sens --help
poetry run subtitlecore_parse2text --help
```

### Create sphinx docs
```
poetry shell
cd apidocs
sphinx-apidoc -f -o source ../subtitlecore
make html
python -m http.server -d build/html
```

### Host docs on github pages
```
cp -rf apidocs/build/html/* docs/
```

### Build
* Change `version` in `pyproject.toml` and `subtitlecore/__init__.py`
* Build python package by `poetry build`

### Git commit and push

### Publish from local dev env
* Set pypi test environment variables in poetry, refer to [poetry doc](https://python-poetry.org/docs/repositories/)
* Publish to pypi test by `poetry publish -r test`

### Publish through CI 

* Github action build and publish package to [test pypi repo](https://test.pypi.org/)

```
git tag [x.x.x]
git push origin master
```

* Manually publish to [pypi repo](https://pypi.org/) through [github action](https://github.com/qishe-nlp/subtitlecore/actions/workflows/pypi.yml)

