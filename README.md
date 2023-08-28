# Peg solitaire solver

## Description
Peg solitaire, also known as **Resta um**, is a board game where the objective is to remove pegs from the board until only one remains. Pegs are removed by jumping over them with another peg.

This program cam figure out if a given board is solvable and, if so, it will output the steps to solve it.

## Usage
In order to run the program, you must have [Python](https://www.python.org/downloads/) installed. Then, run the following command in the terminal:
```bash
python peg.py <input_file>
```
`<input_file>` is the path to a .txt file containing the board to be solved. Like the file `games/default.txt`:
```
##ooo##
##ooo##
ooooooo
oooxooo
ooooooo
##ooo##
##ooo##
```
