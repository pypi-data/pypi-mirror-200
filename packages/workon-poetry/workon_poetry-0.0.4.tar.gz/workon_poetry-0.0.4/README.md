# workon-poetry

Bash and Python scripts to make switching and starting projects more efficient and less error-prone by automating some of the boring stuff and incorporating some opinions about best practices.

## Dependencies

* poetry
* virtualenv

## Setup your Python environment

Launch a `terminal` on Linux (or `git-bash` on Windows) then:

1. Update your pip and virtualenv packages
2. Clone the `workon-poetry` project
3. Create a virtualenv within the `workon-poetry` dir
4. Activate your new Python virtual environment
5. Install this Python package in "--editable" mode

Any Python version greater than `3.7` should work.
As of 2023 most Linux systems use Python `3.9` or higher: 

```bash
pip install --upgrade virtualenv poetry
git clone git@gitlab.com:tangibleai/community/workon-poetry
cd workon-poetry
python -m virtualenv --python 3.9 .venv
ls -hal
```

You should see a new `.venv/` directory.
It will contain your python interpreter and a few `site-packages` like `pip` and `distutils`.

Now activate your new virtual environment by sourcing `.venv/bin/activate` (on Linux) or `.venv/scripts/activate` (on Windows).

```bash
# bin/activate on Linux OR `Scripts/activate` in git-bash on Windows
source .venv/bin/activate || source .venv/Scripts/activate
```

## Developer install

Once you have a shiny new virtual environment activated you can install `workon-poetry` in `--editable` mode.
This way, when you edit the files and have the package change immediately.

Make sure you are already within your cloned `workon-poetry` project directory.
And makes sure your virtual environment is activated.
You should see the name of your virtual environment in parentheses within your command line prompt, like `(.venv) $`.
Then when you install `workon-poetry` it will be available for import within any other Python application in that virtual environment.

```bash
pip install --editable .
```

## User install

If you don't want to contribute, and you just want to **USE** `workon-poetry` the MathText modules, you can install it from a binary wheel on PyPi:

```bash
pip install workon-poetry
```

