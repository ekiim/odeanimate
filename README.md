# ODE Animate

This project aims to be a set of tools for solving,
plotting, and animating _ordinary differential equations_,
solutions.

> The rational for this is, _trying to use pure-python_ to do
numerical analysis.

Most techniques here are going to be without the use of any
external modules.

The only external modules that are used _directly_ by this
project are:

 - `matplotlib`, which is used to configure the _figures_ for plotting.
 - `ffmpeg-python`, which is used to _gather_ several _figures_ and turn them in to
 animations.


## Features

> Most of this features are _W.I.P._ (work in progress)

 - [ ] Vector objects with _basic_ operations.
 - [ ] Function utilities for _real valued_ functions.
 - [ ] Generic _ODE_ integrators.
 - [ ] Automatic plotting for _real valued_ functions.
 - [ ] Utilities for 3D curves.
 - [ ] Utilities for 3D surfaces.
 - [ ] Animation Loop.

## Development

In order to work with this project, perform all executions using [`pipenv`](https://pipenv.pypa.io/en/latest/).

 - Install the project `pipenv install` (do it when ever you update the `Pipfile` at least).
 - `pipenv run python` will run `python` with the configuration required to use this project.
 - `pipenv run <script-name>`, will execute `script.<script-name>` from the `Pipfile`.

