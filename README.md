# ODE Animate

This project aims to be a set of tools for solving, plotting, and animating curves and fields.

> The rational for this is, _trying to use pure-python_ to do numerical analysis.

Most techniques here are going to be without the use of any external modules.

The only external modules that are used _directly_ by this project are:

 - `matplotlib`, which is used to configure the _figures_ for plotting.
 - `ffmpeg-python`, which is used to _gather_ several _figures_ and turn them in to animations.
 - `black`, `coverage` and `pytest` to ensure code quality.


## Features

> Most of this features are _W.I.P._ (work in progress)

 - [X] Vector objects with _basic_ operations.
 - [X] Function utilities for _real valued_ functions.
 - [WIP] Generic _ODE_ integrators.
 - [X] Automatic plotting for _real valued_ functions.
 - [ ] Utilities for 3D curves.
 - [ ] Utilities for 3D surfaces.
 - [ ] Animation Loop.

## Development

In order to work with this project, perform all executions using [`pipenv`](https://pipenv.pypa.io/en/latest/).

 - Install the project `pipenv install --dev`
    - (do it when ever you update the `Pipfile` at least).
 - `pipenv run python` will run `python` with the configuration required to use this project.
 - `pipenv run lint` should run the code linter.
 - `pipenv run format`.
 - `pipenv run tests` should run the test suit, and report back any fails.
 - `pipenv run jupyter lab` should run you a jupyter instance to work on top of the project.

> If you are adding any new script you can added to be executed as
> `pipenv run <script-name>`, in the `Pipfile`.


## Contribute

If you wish to contribute you can contact me directly, or open an issue in the github repository.
The main development for this module is done in a private repository, but for visibility and public
interaction I'll host this in github too.

## License

This project is under the GPL2 License.
