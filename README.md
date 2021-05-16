# connect4

## Set up git hooks
To set up the git hooks, simply run in the root directory:

```bash
make git-hooks
```

This will create a `.git/hooks` directory if none exist and and will symlink the content of `.githooks` into it.

The current `pre-commit` hook supports file formatting using `black` and `isort`.

# Other notes
The game has been impletented using Python 3.6