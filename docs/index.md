# ODE Animate

[![PyPI version](https://badge.fury.io/py/odeanimate.svg)](https://pypi.org/project/odeanimate/)

This project aims to be a set of tools for solving, plotting, and animating curves and fields.

> The rational for this is, _trying to use pure-python_ to do numerical analysis.

Most techniques here are going to be without the use of any external modules.

The only external modules that are used _directly_ by this project are:

 - `matplotlib`, which is used to configure the _figures_ for plotting.
 - `ffmpeg-python`, which is used to _gather_ several _figures_ and turn them in to animations.


## Features

> Most of this features are _W.I.P._ (work in progress)

 - [x] Vector objects with _basic_ operations.
 - [x] Function utilities for _real valued_ functions.
 - [x] Automatic plotting for _real valued_ functions.
 - [ ] Generic _ODE_ integrators.
 - [ ] Utilities for curves.
 - [ ] Utilities for surfaces.
 - [ ] Animation Loop and widgets

## Development

> Initially this project was developed with [`pipenv`](https://pipenv.pypa.io/en/latest/), but for publishing pourpuses
> I decided to change to [Poetry](https://python-poetry.org/).

In order to install the project for development (meaning you are intending to work with it to extend it's capabilities, or improve it's documentation),
you should make sure you have poetry installed in your machine (check the link above), and simply execute `poetry install`, 
and after you can start running python commands with it as

 - `poetry run python` will run `python` with the configuration required to use this project.
 - `poetry run jupyter lab` should run you a jupyter instance to work on top of the project.
 - `poetry run ./scripts/lint.sh` should run the code linter.
 - `poetry run ./scripts/format.sh`, to format the code.
 - `poetry run ./scripts/tests.sh` should run the test suit, and report back any fails.
 - `poetry run ./scripts/docs.sh` to build the documentation html site.

## Contribute

If you wish to contribute you can contact me directly, or open an issue in the github repository.
The main development for this module is done in a private repository, but for visibility and public
interaction I'll host this in github too.

## License

This project is under the [GPL2 License](/LICENSE.txt).
