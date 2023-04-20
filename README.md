# ODE Animate

[![PyPI version](https://badge.fury.io/py/odeanimate.svg)](https://pypi.org/project/odeanimate/)

This project aims to be a set of tools for solving, plotting, and animating curves and fields.

> The rational for this is, _trying to use pure-python_ to do numerical analysis.

Most techniques here are going to be without the use of any external modules.

The only external modules that are used _directly_ by this project are:

 - `matplotlib`, which is used to configure the _figures_ for plotting.


## Features

> Most of this features are _W.I.P._ (work in progress)

 - [x] Vector objects with _basic_ operations.
 - [x] Vector objects with _basic_ operations.
 - [x] Function utilities for _real valued_ functions.
 - [x] Automatic plotting for _real valued_ functions.
 - [ ] Generic _ODE_ integrators.
 - [X] Utilities for curves.
 - [ ] Utilities for surfaces.
 - [ ] Animation Loop and widgets

## Development

> This project uses [`pipenv`](https://pipenv.pypa.io/) for local development and testing.

If you are intending to:

- Add examples or documentation,
- develop further this module
- use and test in an isolated enviroment

you should have `pipenv` installed.

One you cloned the repository, you should be able to execute `pipenv install --dev` and everything should be working.

Most of what you would need is configured in the `pyproject.toml` file, so if you are using the tools specified in
the `scripts` section of the `Pipfile` you should be fine.

## Contribute

If you wish to contribute you can contact me directly, or open an issue in the github repository.
The main development for this module is done in a private repository, but for visibility and public
interaction I'll host this in github too.

## License

This project is under the [GPL2 License](/LICENSE.txt).
