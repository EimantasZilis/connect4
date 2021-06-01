# connect4

## Set up git hooks
To set up the git hooks, simply run in the root directory:

```bash
make git-hooks
```

This will create a `.git/hooks` directory if none exist and and will symlink the content of `.githooks` into it.

The current `pre-commit` hook supports file formatting using `black` and `isort`.

# To do
 - Update readme
 - Fix environment file and make sure environment gets created correctly
 - rename connectz.py to main.py
 - move stuff to utils/helper files
 - write unit tests
 - remove sys.exits
 - raise exceptions?


