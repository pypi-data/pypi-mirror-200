# Google-Driver
![YouTuber](https://img.shields.io/badge/pypi-googledriver-blue)
![Pypi Version](https://img.shields.io/pypi/v/googledriver.svg)
[![Contributor Covenant](https://img.shields.io/badge/contributor%20covenant-v2.0%20adopted-black.svg)](code_of_conduct.md)
[![Python Version](https://img.shields.io/badge/python-3.6%2C3.7%2C3.8-black.svg)](code_of_conduct.md)
![Code convention](https://img.shields.io/badge/code%20convention-pep8-black)
![Black Fomatter](https://img.shields.io/badge/code%20style-black-000000.svg)

The Python package google drive facilitates access to files uploaded to Google Drive.

<br>

# Installation
```
pip install googledriver
```

<br>

# Features
`Simple Download` <br>
To save a file from a shared Google Drive URL to local storage, use the following code.
```python
from googledriver import download

URL = 'https://drive.google.com/file/d/xxxxxxxxx/view?usp=share_link'
download(URL, './model/tf_gpt2_model')
```

<br>

`Download as Cached` <br>
To download a cached file (or directory) from a URL and return its path, you can use the following method.

```python
from googledriver import download

URL = 'https://drive.google.com/file/d/xxxxxxxxx/view?usp=share_link'
cached_path = download(URL, None, 'tf_model')
```
Basically, torch cached is used, and the huggingface hub module is used as a reference and wrapped.

<br>

# References
[1] https://github.com/huggingface/transformers