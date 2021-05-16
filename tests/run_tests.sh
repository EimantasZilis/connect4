#!/bin/zsh

echo ">> draw - expected 0"
python ../connectz.py files/draw.txt

echo "\n>> illegal column - expected 6"
python ../connectz.py files/illegal_column.txt

echo "\n>> illegal continue - expected 4"
python ../connectz.py files/illegal_continue.txt

echo "\n>> illegal game - expected 7"
python ../connectz.py files/illegal_game.txt

echo "\n>> illegal row - expected 5"
python ../connectz.py files/illegal_row.txt

echo "\n>> incomplete - expected 3"
python ../connectz.py files/incomplete.txt

echo "\n>> invalid file - expeceted 8"
python ../connectz.py files/invalid_file.txt

echo "\n>> player 1 win (left-diagonal) - expected - 1"
python ../connectz.py files/player_1_win_left_diagonal.txt

echo "\n>> player 1 win - expected - 1"
python ../connectz.py files/player_1_win.txt

echo "\n>> player 2 win (horizontal) - expected - 2"
python ../connectz.py files/player_2_win_horizontal.txt

echo "\n>> player 2 win (right-diagonal) - expected - 2"
python ../connectz.py files/player_2_win_right_diagonal.txt

echo "\n>> player 2 win - expected - 2"
python ../connectz.py files/player_2_win.txt
