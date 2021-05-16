The code was implemented using Python 3.6

Assumptions
1. I assumed that the input files are going to be large. 
I used generators to read files line by line and avoid putting the whole file into memory
2. I assumed that the first line can be in any order, not just "X Y Z". 

How winning games are being checked.
Looping through every possible row, column and diagonal line at each move is expensive.
To cut down the number of loops, it is important to note that we do not have
to check every piece on the board. At the end of each move, we know that a piece will always
land at the top of the column. By taking the newest piece as a starting position, we only
need to check:
 - The column below
 - The diagonal lines going down on the left and right
 - The horizontal line with the newest piece in the middle.  

The code also does not check if the game has been won unless the minimum number of moves have
been made already.

Improvements
 - Write unit tests for connectz.py module
 - Define many different input games to test the code with
 - Test the code with large file

Challenges with the coding Challenge
All in all, I enjoyed working on this puzzle. The game specification was also very detailed and I think it can be easy to miss or overlook certain requirements.
With that in mind, I also think that it is easy to get into the rabbit hole and try to over engineer the solution.