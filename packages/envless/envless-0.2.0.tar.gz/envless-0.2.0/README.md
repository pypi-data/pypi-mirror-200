# envless: a python utility for running scripts with dependencies declared inline

Python scripts are great and useful, but for simple tasks that require a
dependency or two, it can be annoying to manage virtualenvs. This is especially
annoying if you want to write the scripts to manage your dev environment in python.

`envless` provides a self-contained way for python scripts to declare and load
their dependencies. To make the idea clearer, here's an example script that
fetches and prints the `python.org` site:

```python
import envless

envless.script_dependencies({"requests": "==2.28.2"}, __file__)

import requests

response = requests.get("https://python.org")
print(response.text)
```

In short, this will run the script, installing `requests` if needed, so that
you don't need to have it preinstalled or set up a virtualenv or anything
first. If this script is called `show_python.py`, then you just run `python
show_python.py`, and it works!

This is heavily inspired by how
[deno](https://deno.land/manual@v1.31.3/examples/manage_dependencies) and
[go](https://go.dev/blog/using-go-modules) automatically determine dependencies
based on the source code rather than declaring them manually in a separate file.

## Installation

The only requirement is that you need to be able to `import envless` when
you're running the python you want to use for the script. This usually means
that you should `pip install --user envless`.

If you have multiple versions of python on your system, this means you should
install with the corresponding `pip`. So if your system default python is 3.8,
but you also have 3.11 installed, and you want to run with 3.11, you might need
to `pip3.11 install --user envless` and then `python3.11 <script>` to run your
script.

`envless` should always support all
[currently supported python versions](https://devguide.python.org/versions/),
except python3.7, which is about to go end-of-life at the time of writing this
package.

## How it works

The `script_dependencies` function turns the requirements dict into a
`requirements.txt` tempfile. It then hashes that tempfile and the running
python version to get a version ID, creates a virtualenv with that ID if
needed, and installs the dependencies into that virtualenv. Then it `exec`s the
current interpreter with that virtualenv active so that the dependencies are
available to the script.

Note that this implies that the dependencies do not contaminate your global
environment, and also that virtualenvs can be shared among scripts with the
same dependency declarations (so don't go messing with them manually).

If you want to clear out old envs, they live in your platform's equivalent of
`~/.local/share/envless/virtualenvs`. It should always be safe to delete this
directory if there isn't a script actively running; envs will be recreated as
needed.

## API

`envless.script_dependencies`: the only function in the package you should need
to use from your code.

Args:
- `requirements`: a `dict` where keys are package names that can be installed
  via `pip` and values are version specifiers for those packages (again, any
  version specifier that `pip` can handle). If you don't care about the version
  you get, just pass `""` as the version specifier.
- `source_file`: the path of the file that is calling this function. You should
  always just pass the python builtin variable `__file__` for this argument.

## Examples

See the `tests` dir, which contains scripts that use `envless`.

## Limitations

Your call to `envless.script_dependencies` must come before you import any code
outside the standard library.

`envless` only works well when used in the script that you're using as an
entrypoint. Importing another script that uses envless will end up executing
that other script as the entrypoint, which is probably not what you want. If
you think you might need to import a script that uses envless, you can put the
call to `envless.script_dependencies` inside an `if __name__ == "__main__":`
block (which still must occur prior to any imports outside the standard
library). For example:
```python
if __name__ == "__main__":
    import envless
    envless.script_dependencies({"requests": "==2.28.2"}, __file__)

import requests

response = requests.get("https://python.org")
print(response.text)
```

Note, however, that this means that the script doing the importing is
responsible for providing all the dependencies; in this example, `requests`
will not be installed automatically if the script is not the entrypoint.

