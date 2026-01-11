# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/danieljmehler/esri-cli/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                             |    Stmts |     Miss |   Cover |   Missing |
|--------------------------------- | -------: | -------: | ------: | --------: |
| cli.py                           |      297 |       39 |     87% |144-158, 180, 231, 268, 298, 303-306, 334-335, 338, 366-367, 391-395, 410, 422-423, 464, 470, 492, 511, 513 |
| example.py                       |       11 |       11 |      0% |      1-21 |
| setup.py                         |        2 |        2 |      0% |       1-3 |
| src/esri\_client/\_\_init\_\_.py |        6 |        0 |    100% |           |
| src/esri\_client/client.py       |       58 |       35 |     40% |44-45, 49-51, 55-69, 72-75, 78-81, 84-87, 90-93 |
| src/esri\_client/folder.py       |        8 |        0 |    100% |           |
| src/esri\_client/layer.py        |       30 |        5 |     83% |43, 54, 60, 64-65 |
| src/esri\_client/service.py      |       12 |        1 |     92% |        20 |
| src/esri\_client/services.py     |        9 |        0 |    100% |           |
| tests/test\_cli.py               |      437 |        0 |    100% |           |
| tests/test\_client.py            |       16 |        0 |    100% |           |
| tests/test\_layer.py             |       19 |        0 |    100% |           |
| tests/test\_services.py          |       10 |        0 |    100% |           |
| **TOTAL**                        |  **915** |   **93** | **90%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/danieljmehler/esri-cli/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/danieljmehler/esri-cli/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/danieljmehler/esri-cli/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/danieljmehler/esri-cli/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Fdanieljmehler%2Fesri-cli%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/danieljmehler/esri-cli/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.