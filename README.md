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
 - write unit tests


