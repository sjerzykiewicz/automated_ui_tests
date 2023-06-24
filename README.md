# automated_ui_tests
Automated UI tests for [saucedemo](https://www.saucedemo.com/) app

## Requirements
- Python 3.11.1
- Firefox browser

## Installation
1. Clone the repository

    `git clone https://github.com/sjerzykiewicz/automated_ui_tests.git` 

2. Create a virtual environment

    `virtualenv .venv`

3. Install dependencies

    `.venv/Scripts/pip install -r requirements.txt`

4. If you do not have Firefox browser already installed, download it from [here](https://www.mozilla.org/en-US/firefox/new/)

## Running tests
1. Run pytest

    `.venv/Scripts/pytest`

## GitHub Actions
Tests are run automatically on every push to the main branch. You can find the results [here](https://github.com/sjerzykiewicz/automated_ui_tests/actions/)