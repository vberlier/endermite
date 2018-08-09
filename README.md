# endermite

[![Build Status](https://travis-ci.com/vberlier/endermite.svg?branch=master)](https://travis-ci.com/vberlier/endermite)
[![PyPI Version](https://img.shields.io/pypi/v/endermite.svg)](https://pypi.org/project/endermite/)
[![Python Version](https://img.shields.io/pypi/pyversions/endermite.svg)](https://pypi.org/project/endermite/)

> A high-level, opinionated python framework for building [Minecraft data packs](https://minecraft.gamepedia.com/Data_pack).

**🚧 This is a huge work in progress 🚧**

## Introduction

[Minecraft data packs](https://minecraft.gamepedia.com/Data_pack) make it possible for anyone to customize the game by writing bits of JSON and a few functions. The underlying format is simple and straight-forward, making it easy to parse, but it hasn't been created with a specific developer experience in mind. When you sit down in front of your text editor, it can be hard to figure out how you're supposed to make use of the available features to do what you want to do.

Endermite is a python framework that combines and exposes data pack features through a layer of abstraction. It aims to make it easier to develop, encapsulate and compose behavior by providing a component-based approach.

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

## Getting started

The easiest way to get started with endermite is to get familiar with the command-line workflow. You can use endermite without it but the `ender` CLI will usually allow you to be much more productive.

```sh
$ ender --help
Usage: ender [OPTIONS] COMMAND [ARGS]...

  Command-line utility to manage endermite projects.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  build  Build all the projects of the current world.
  init   Create a new endermite project.
```

### Creating a new project

The `ender` CLI lets you create an endermite project inside of a Minecraft world folder by running the `init` command. Note that you can create as many endermite projects as you want in the same world.

```sh
$ ender init
endermite vX.X.X

Creating endermite project.

Project name [testing_endermite]: tutorial
Project description [An endermite project]:
Project author [N/A]:
Project version [0.1.0]:

About to create .../.minecraft/saves/testing_endermite/@endermite/tutorial.

Is this ok? [Y/n]:

Done!
```

The project created by the `ender` CLI is simply a python package that exports an endermite `Project` object.

### Building your endermite projects

You can use the `build` command to build all the projects you created in a specific Minecraft world. The command will output the corresponding data packs in the `datapacks` directory.

```sh
$ ender build
endermite vX.X.X

Building endermite projects.

Attempting to build "tutorial"...
Done! (took X.XXXs)
```

Running the `build` command with the `--watch` option will rebuild your projects whenever you make modifications to the `@endermite` directory. It lets you forget about having to run the `build` command manually.

```sh
$ ender build --watch
endermite vX.X.X

Building endermite projects.

Watching directory .../.minecraft/saves/testing_endermite/@endermite.

HH:MM:SS X changes detected

Attempting to build "tutorial"...
Done! (took X.XXXs)
```

Remember that you still need to run `/reload` in-game.

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
