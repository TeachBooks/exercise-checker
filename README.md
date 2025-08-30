# Exercise Checker

**Update, Aug 30, 2025:** _version `v1.0.0` is released and is ready for texting in educational settings! Until Issue #13 is completed, the Python files should be deployed in the same working directory as the book page in which they are used._

The *Exercise Checker* package is designed to streamline the creation and evaluation of exercises in Jupyter notebooks, and is in particular designed for use as on a page within a Jupyter Book. Teachers can define exercises using a dictionary in a notebook cell, ensuring a simple and intuitive setup. Once the *Checker* package is imported, it generates all necessary checking functions automatically, enabling seamless integration with the notebook. This approach minimizes the need for writing repetitive code, allowing educators to focus on content creation and providing students with an efficient and interactive learning experience. The tool is written in Python, the teacher defines the exericse using Python dictionaries and the student "submits" answers to be checked by writing Python and clicking the "check answer" button.

This tool is designed with teachers in mind who are using the Python programming language to help students learn topics in science and engineering, in particular those who may not have a strong grasp on programming in general, or the Python language specifically. It is possible to provide feedback and hints via the "check answer" button such that students focus on the topic of interest, and avoid students being distracted with Python errors (unless that is the intent of the activity or exercise). To make exercise creation as easy as possible, a teacher defines it using a Python dictionary only, along with a few simple lines of code.

For now, the best way to understand this tool is to read the contents of `check.py` (documentation will be implemented later) and to look through the examples in the notebooks in the `development/` directory. Key features are:

- easily define exercises and feedback using a Python dictionary
- automatically create a "check answer" button (text on button is customizable)
- customize feedback for right or wrong answers after pressing buttons (e.g., hints)
- check various Python objects: numeric values, functions, strings, object type
- check correct answers using various tolerance criteria (absolute, relative, inside/outside limits)
- list allowed types for numeric value answers and (optionally) inform students of compliance via feedback

Anyone is encouranged to use this tool and provide feedback via GitHub Issues in this repository. The following developments will be made in parallel:

1. Create and use new exercises (please let us know how by linking to your book in a GitHub Issue!).
1. Example deployment and usage of exercises in a Jupyter Book/TeachBook (Issue #15).
2. Set up documentation describing usage and example exercises (Issue #11).
3. Set up PyPI releases (Issue #13).
4. Implement testing framework (Issue #12).

The original concept for this tool was created by Max Guichard in the summer of 2023 for use in the MUDE Textbook. Robert Lanzafame, as usual, came up with an infinite list of new features; luckily Federico Raimondi did an excellent job of translating these ideas into something practical and feasible, resulting in the dictionary-powered customizable implmentation released in `v1.0.0` (August, 2025).

## Usage

There are two discting ways in which this tool is used: 1) creation of exercises, by the teacher, and 2) deployment of the exercises in a notebook setting, for interactive use with students.

At the moment, the best way to develop an exercise is to clone this repository (or download the files) and use notebooks `00.ipynb` and `01.ipynb`. Once an exercise is ready, use notebook `02.ipynb` to help deploy it in your Juypter Book. Note that at the moment a working example in a book is not ready, so you may need to modify the code provided in this repo to get everything working smoothly in your book.

### Creating Exercises

First step is creating a decorator function `check` that will create the check answer button and allow the student to check their answer with the correct solution.

This is the minimum usage of the tool, which will create a functional "check answer" button when run in a Jupyter notebook cell:

```python
from exercise_checker.check import check_example
exercise = {}
check_example(globals(), exercise)
```

The conventional usage will be more like this:

1. `from exercise_checker.check import check_example`
2. Define the exercise in a dictionary
3. Write the code to complete the exercise
4. Run `check_example(globals(), exercise)` to create the "check answer" button

In most applications this can be accomplished in three cells, where Items 1 and 2 can be combined in the first cell.

### Deploying and Using Exercises with Students

This tool is designed with the expectation that exercises (dictionaries) are used by students in an interactive setting with a notebook-based Python interpreter, specifically: a Jupyter Book page using the Sphinx-Thebe extension (see the [TeachBooks Manual page](https://teachbooks.io/manual/features/live_code.html)). This allows a teacher to easily hide the source files and/or exercise initialization code from the student (e.g., with custom cell tags).

Until the PyPI deployment is ready, the code in `check.py` will need to be deployed within your book. This is roughly described in notebook `02.ipynb`.

**Coming soon:** example book illustrating deployment and usage of the exercise checker.

## Repository Structure

The source code is in `exercise_checker/`, which is currently a local package, but will eventually become the PyPI package source code. The `development/` directory contains notebooks that are used to develop the package and test its functionality. These will eventually be converted into tests and stored in the `tests/` directory.

```
exericise_checker
├── exercise_checker
|  ├── __init__.py
|  ├── checker.py
|  └── ...
├── development
|  ├── 01.ipynb
|  ├── 02.ipynb
|  └── 
├── tests
|  └── empty for now
```

## Development

Development should be done in arbitrarily numbered notebooks. When new features are added, create a new notebook that tests only that new functionality.

New Python code can be developed in a notebook cell, but should be added to the module when a branch is merged into `main`.

The process of "testing" is simply running each notebook manually and checking that the "check answer" button works as expected.

Each notebook contains cells that set up the development environment properly:

- autoreload allows the module to be edited and reloaded in the notebook environment without restarting the kernel
- the `exercise_checker` directory is added to the system path to allow conventional importing of the module 

### Python Environment

If using VS Code, a development environment can be created as follows:

```bash
pip install -e .[dev]
```

Leave off the `[dev]` if not using VS Code (i.e., `pip install -e .`). Note that the editable mode on Windows can sometimes be very slow; if so, leave this option out (development can still be carried out using notebooks only with `autoreload`).

### Releases

Version `v1.0.0` was released in August, 2025 and uses semantic versioning. Only changes that alter the behavior of the exercise checker itself will advance the major version number (i.e., `v1` to `v2`). Improvements such as documentation pages, PyPI releases, etc, will advance the minor version number.

## Unprocessed Notes

_These are the notes from Robert/Federico's meeting in November._

goal for usage is this:
- teacher defines the exercise using only a dictionary defined in a notebook cell
- exercise checker is imported in a cell and can be used to do everything in the notebook
- checking functions are created automatically

repo management and development
- start describing the types of checks and things like that in the readme
- lets also add example usage there
- send sketches via teams could be a good brainstorming mechanism

Stages for an check that checks values
- list desired values 
- checker.float(3, 12, 23 32 )
- or this: checker.float(dict): {names: ['x1, x2' ...], values=[2, 43,53242,34], other?, type, tol, hints/answers}
- .... needs to be worked out more

let's come up with a few more (simple) exercises
- additions, functions, exponents,...
- write out in comments in a py or ipynb file
- focus on numerical stuff for now

**Implementation**

Original setup works by running `check_example(globals())`, which is defined in a separate `*.py` file (there is also the button - defined in another `*.py` file). In total this required 3 files; 2 too many!

New setup:
- import checker (for now this is just a local module) (use autoreload cell magic)
- define an exercise entirely within a dictionary
- do the exercise
  - create button by running this in a cell: `check(dict, globals())`
  - imagine you want two exercises on one page. then:
    - create a new dictionary
    - `check(dict2, globals())`
