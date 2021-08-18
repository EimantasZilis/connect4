# connect4

This repo contains a game checker software based on the [Connect4](https://en.wikipedia.org/wiki/Connect_Four) game. While the traditional game is based on 6 x 7 grid with 4 pieces required to win, the software was generalised to arbitrary numbers and sizes. It can check any game of any grid size and any number of pieces required to win.

To run the game checker, install Python 3.9 and use:
```
python check_game.py path_to_game_file
```
It takes filepath as a single argument that describes the game setup and moves taken. It will play through the game in the background and will summarise if the game has been won, drawn or if there has been some kind of an error.

## How it works
### Inputs: the game file
In order to check the game, a filepath needs to be specified. It should point to a text-based file that has the following format:

1. The first line describes the game setup and is composed of three space-delimited integers such as
```
4 5 3
```
where
 - `4` represents the number of columns on the board
 - `5` represents the number of rows 
 - `3` represents the minimum number of pieces in a row required to win the game.

The traditional game is played on a 7 x 6 board with 4 pieces required to win. This would be described using
```
7 6 4
```

2. The rest of the file is used to described the player moves. Each line represents a move starting with player one and alternates between both players on each line. A move is desribed by a single positive integer indicating which column the player chose to drop the piece in. The file should end after the game has been won or drawn. Any additional moves will be detected as an invalid game.

For example, the following game represents a 3 x 4 game with 3 moves required to win:
```
3 4 3
1
2
3
1
3
3
1
3
2
```
This particular game is won by player 1 because there three pieces in a row along a diagonal:
```
| | |2|
|1| |2|
|2|1|1|
|1|2|1|
```
where numbers 1 and 2 represent the players' pieces. More game examples can be found in
```
tests/sample_games/
```

### Impossible games
With the way game files are specified, it is possible to run into games that are not valid or are impossible to win. For example:
```
2 4 6
```
There is no way to achieve 6 pieces in a row in a board that is 2 x 4. Situations similar to this are classified as illegal games and return a corresponding output.

### Outputs
The checker pogram can return one of the ten status:

| Game Status                  | Description |
|------------------------------|--------|
| Game Over: Draw              |        |
| Game Over: Player 1 win      |        |
| Game Over: Player 2 win      |        |
| Game Error: Incomplete Game  | The game has not been finished and there are valid moves xpossible, but none were taken |
| Game Error: Illegal Continue | Players cannot make moves after the game is finished" |
| Game Error: Illegal Row      | Players cannot put pieces in a row that does not exist |
| Game Error: Illegal Column   | Players cannot put pieces in a column that does not exist |
| Game Error: Illegal Game     | The game description is valid, but the game could never be won |
| Game Error: Illegal File     | The game description is not valid or described a game that is impossible |
| Game Error: File Error       | The file cannot be found, opened or read for some reason |

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


