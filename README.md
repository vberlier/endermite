# endermite

[![Build Status](https://travis-ci.com/vberlier/endermite.svg?branch=master)](https://travis-ci.com/vberlier/endermite)
[![PyPI Version](https://img.shields.io/pypi/v/endermite.svg)](https://pypi.org/project/endermite/)
[![Python Version](https://img.shields.io/pypi/pyversions/endermite.svg)](https://pypi.org/project/endermite/)

> A high-level, opinionated python framework for building [Minecraft data packs](https://minecraft.gamepedia.com/Data_pack).

**🚧 This is a huge work in progress 🚧**

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
