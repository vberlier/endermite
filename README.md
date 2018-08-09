# endermite

[![Build Status](https://travis-ci.com/vberlier/endermite.svg?branch=master)](https://travis-ci.com/vberlier/endermite)
[![PyPI Version](https://img.shields.io/pypi/v/endermite.svg)](https://pypi.org/project/endermite/)
[![Python Version](https://img.shields.io/pypi/pyversions/endermite.svg)](https://pypi.org/project/endermite/)

> A high-level, opinionated python framework for building [Minecraft data packs](https://minecraft.gamepedia.com/Data_pack).

**🚧 This is a huge work in progress 🚧**

## Introduction

[Minecraft data packs](https://minecraft.gamepedia.com/Data_pack) make it possible for anyone to customize the game by writing bits of JSON and a few functions. The underlying format is simple and straight-forward, making it easy to parse, but it hasn't been created with a specific developer experience in mind. When you sit down in front of your text editor, it can be hard to figure out how you're supposed to make use of the available features to do what you want to do.

Endermite is a python framework that combines and exposes data pack features through a level of abstraction. It aims to make it easier to develop, encapsulate and compose behavior by providing a component-based approach.

```python
from endermite import Component
from endermite.decorators import public, tick


class Hello(Component):
    """Output `Hello, world!` each tick when attached to an entity."""

    @tick
    @public
    def say_hello(self):
        self.say('Hello, world!')
```

Components are coupled pieces of state and behavior that can be attached to entities. They're conceptually similar to what you might be used to with `MonoBehaviour` scripts if you've worked with the Unity game engine.

## Installation

Make sure that you're using Python 3.7 or above. You can install endermite with `pip`.

```sh
$ pip install endermite
```

You can check that endermite is correctly installed by trying to use the command-line interface shipped with the package.

```sh
$ ender --version
```

## Contributing

Contributions are welcome. Make sure that Python 3.7 or newer is installed and create a virtual environment in the project directory.

```sh
$ python -m venv env
```

This will create a virtual environment in the `env` directory. If you're not familiar with virtual environments, please check out the [official documentation](https://docs.python.org/3/tutorial/venv.html). You can now activate the virtual environment.

```sh
# Windows
$ env\Scripts\activate.bat

# Unix or MacOS
$ source env/bin/activate
```

Remember to activate the virtual environment every time you work on the project! Let's install the dependencies for the `endermite` package and the necessary development dependencies.

```sh
(env) $ pip install -U -r requirements.txt -r requirements.dev.txt
```

You should now be able to lint the source code and to run the tests with `tox`.

```sh
(env) $ tox
```

The project relies on [`pylint`](https://www.pylint.org/) and [`pytest`](https://docs.pytest.org/en/latest/) for linting and testing. If you're not familiar with these tools, you can check out their respective documentation.

---

License - [MIT](https://github.com/vberlier/endermite/blob/master/LICENSE)
