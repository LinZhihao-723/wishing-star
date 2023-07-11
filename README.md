# Wishing Star

This is the customized Discord Bot developed by myself.

## Development

1. Create and enter the virtual environment:
   `python3.x -m venv v3x; . ./v3x/bin/activate`
2. Update `pip`:
   `pip install --upgrade pip`
3. Install the project in editable mode along with the development dependencies:
   `pip install -e .[dev]`

## Start

To start the bot, a valid credential token should be provided:
`python start.py --key $KEY_VAL`

## Contributing

Before submitting a pull request, run the following error-checking and
formatting tools:

* [mypy][1]: `mypy src`
  * mypy checks for typing errors. You should resolve all typing errors or if an
    error cannot be resolved (e.g., it's due to a third-party library), you
    should add a comment `# type: ignore` to [silence][2] the error.
* [docformatter][3]: `docformatter -i src`
  * This formats docstrings. You should review and add any changes to your PR.
* [Black][4]: `black src`
  * This formats the code according to Black's code-style rules. You should
    review and add any changes to your PR.
* [ruff][6]: `ruff check --fix src`
  * This performs linting according to PEPs. You should review and add any
    changes to your PR.

Note that `docformatter` should be run before `black` to give Black the [last][5].

[1]: https://mypy.readthedocs.io/en/stable/index.html
[2]: https://mypy.readthedocs.io/en/stable/common_issues.html#spurious-errors-and-locally-silencing-the-checker
[3]: https://docformatter.readthedocs.io/en/latest/
[4]: https://black.readthedocs.io/en/stable/index.html
[5]: https://docformatter.readthedocs.io/en/latest/faq.html#interaction-with-black
[6]: https://beta.ruff.rs/docs/
