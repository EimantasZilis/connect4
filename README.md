# connect4

This repo contains a game checker software based on the [Connect4](https://en.wikipedia.org/wiki/Connect_Four) game. While the traditional game is based on 6 x 7 grid with 4 pieces required to win, the software was generalised to work with arbitrary numbers and sizes. It can check any game of any grid size and any number of pieces required to win.

To run the game checker, install Python 3.9 and use:
```
python check_game.py path_to_game_file
```
It takes filepath as a single argument which describes the game setup and moves taken. It will play through the game in the background and will summarise if the game has been won, drawn or if there has been some kind of an error.

## Inputs and outputs
### 1. Inputs: the game file
In order to check the game, a filepath needs to be specified. It should point to a text-based file that has two parts:
 - A header line describing the game setup
 - The rest of the file used to describe moves taken by the players.

#### 1.1 Game setup
The first line in the file describes the game setup and is composed of three space-delimited integers such as
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
#### 1.2 Player moves
The rest of the file after line one describes the player moves. Each line represents a move starting with player one and alternates between both players on each line. A move is desribed by a single positive integer indicating which column the player chose to drop the piece in. The file should end after the game has been won or if there is a draw. Any additional moves will be detected as an invalid game.

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
This particular game is won by player 1 because there three pieces in a row along a diagonal. Visually, this can be represented by:
```
| | |2|
|1| |2|
|2|1|1|
|1|2|1|
```
where numbers 1 and 2 represent the players' pieces. More game file examples can be found in
```
tests/sample_games/
```
#### 1.3 Impossible games
Since the game checker can work with arbitrary numbers and sizes, it is possible to define a game that is not valid or is impossible to win. For example, consider the following setup:
```
2 4 6
```
There is no way to achieve 6 pieces in a row on a board that is 2 x 4. Situations similar to this are classified as illegal games and return a corresponding output.

### 2. Outputs
The checker pogram can return one of the ten status:

| Game Status               | Description |
|---------------------------|--------|
| Draw             | Game has completed successfully with a draw |
| Player 1 win     | Game has completed successfully player 1 winning the game |
| Player 2 win     | Game has completed successfully player 2 winning the game |
| Incomplete Game  | Game error: the game is not finished, but no more moves were taken |
| Illegal Continue | Game error: players cannot make moves after the game is finished |
| Illegal Row      | Game error: players cannot put pieces in a row that does not exist |
| Illegal Column   | Game error: players cannot put pieces in a column that does not exist |
| Illegal Game     | Game error: the game description is valid, but the game could never be won |
| Illegal File     | Game error: the game description is not valid or described a game that is impossible |
| File Error       | Game error: the file cannot be found, opened or read for some reason |

## 3. How it works
Looping through every possible row, column and diagonal lines at each move is expensive. To cut down the number of checks at every turn, two considerations have been taken.

1. Do not check if the game has been won unless the minimum number of winning moves has been made already. 
This is dependent on the game setup. Since the minimum number of winning moves is defined by:
```
minimum_moves_to_win = 2 * required_winning_moves  - 1
```
the code does not check for wins if `total_moves_at_any_time < minimum_moves_to_win`.

1. Only check the relevant pieces around the most recent one - not the whole board.
At the end of each move, we know that a piece will always land at the top of the column. By taking the newest piece as a starting point, the following checks are made in this order:
 - The column below
 - The diagonal (left/right) lines going down
 - The horizontal line with the newest piece in the middle of it
 - The diagonal (left/right) lines going up (in case columns next to them have rows above with pieces).

## 4. Development
For any futher development or changes to this repo (on mac OS), install conda via 
```
brew install anaconda
```
and create `connect4` environment using
```
conda env create -f development/environment.yml
```
Setup git hooks using
```bash
cd development
make git-hooks
```
and it will symlink the content of `.githooks` into it. The current `pre-commit` hook supports file formatting using `black` and `isort` and `autoflake` to ensure consistent formatting.
