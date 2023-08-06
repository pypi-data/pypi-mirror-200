# Contributing to multi-scale-expansion

## Programming Language Prerequisites
Please make sure you have Python 3.7 or above install before you commence contributing. 

## Dependencies 
Run `make develop` to install development dependencies which leverages pip for its subsequent installs. 

## Forking and Cloning 
If you'd like to participate and contribute there's a set of steps you need to take before doing so, we encourage you to follow the github's [contributing to projects guidelines](https://docs.github.com/en/get-started/quickstart/contributing-to-projects)

A set of steps to contribute are: 
- Fork and clone the repository
- Create your own branch for new features 
- Commit and push the changes you've made (please make sure to be as detailed as possible in your commit message)
- Test and lint
- Create a Pull Request (PR)

## Testing and Linting
- It's of utmost importance that before opening a PR you test your code and add new tests for new features, you do so by running `make tests` or `make coverage` if you also want to get coverage information. 
- We also want to conduct static analysis on our code and for such we use `make lint`. 
- To autoformat our library using `black` we use `make format`. 

## Create a PR
If you're confident you've properly tested and your change is ready to be reviewed, navigate to your forked repo on the GitHub website and go to the branch were you've made the changes, choosing to create a PR. 

## Makefile References
- `make`: list available commands
- `make develop`: install and build this library and its dependencies using `pip`
- `make build`: build the library using `setuptools`
- `make lint`: perform static analysis of this library with `flake8` and `black`
- `make format`: autoformat this library using `black`
- `make annotate`: run type checking using `mypy`
- `make test`: run automated tests with `pytest`
- `make coverage`: run automated tests with `pytest` and collect coverage information
- `make dist`: package library for distribution
