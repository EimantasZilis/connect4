# connect4

## Set up git hooks (for development)
To set up the git hooks, simply run in the root directory:

```bash
make git-hooks
```

This will create a `.git/hooks` directory if none exist and and will symlink the content of `.githooks` into it.

The current `pre-commit` hook supports file formatting using `black` and `isort`.

## Installation and setup
On macOS, install conda via 
```
brew install anaconda
```
and create connect4 environment using
```
conda env create -f environment.yml
```

# To do
 - Update readme
 - Fix environment file and make sure environment gets created correctly
 - move stuff to utils/helper files
 - write unit tests
 - remove sys.exits
 - raise exceptions?
 - Fix parser to only accept one argument
 - Remove X/Y/Z headers
 - Remove ASCII dependency


