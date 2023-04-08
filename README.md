# Wordle Solver

This is a wordle soving algorythm that I made. The purpose of this is to test different solving algorythms and not to solve the daily wordle. That is why there is not a very great user interface.

This contains 4 different algorythms:
  * Random Solver
  * Most Common Letter
  * Best Guess (Unoptimized)
  * Best Guess (Optimized)
 
# How It Works

It takes in an answer, runs it through the algorythm and returns the number of guesses it took for the algorytm and the word it choose for each guess. It always uses "salet" as the first guess becuase it is the best possible starting word.


Note: This algorthm only knows how many boxes are green and how many are yellow. It does not know which letters are green and which ones are yellow. This is why it is not always very accurate.

# Algorythms

Here is a break down of each algorythm:

### Random Solver

##### Explination

This is the first algorythm that I made. It is very basic. All it does is picks a random word from the word bank, checks it, then removes everything from the list that does not get the same score when put agaisnt the guess.

##### Stats

Word Bank Size: 14000<br />
Number of Test: 10000

Chance of beating Wordle (<= 6 guesses): 62.03%<br />
Average guesses: 6.2381<br />
Time taken to run: 317.33 seconds<br />

### Most Common Letter

##### Explination

This is a upgraded version of Random Solver. However, instead of just randomly guessing, it figures out the most common letters in the remaining possible answers and picks the word that has the most number of the top 5 most common letters.

##### Stats

Word Bank Size: 14000<br />
Number of Test: 10000

Chance of beating Wordle (<= 6 guesses): 62.97%<br />
Average guesses: 6.2147<br />
Time taken to run: 394.77 seconds<br />


### Best Guess (Unoptimized)

##### Explination

This basically goes through all the options to see what the "best possible guess" would be and then makes that guess. This is very slow since I didnt add any optimization to it. This is why there is no testing data.

##### Stats

Word Bank Size: 14000<br />
Number of Test: 10000

Chance of beating Wordle (<= 6 guesses): N/A<br />
Average guesses: N/A<br />
Time taken to run: N/A<br />


### Best Guess (Optimized)

##### Explination

This is a more optimized version of Best Guess. It usses conditional entropy to find the best guess. It also uses cashe, parallelization and heuristics to optimize the speed. It was tested agains 300+ real past Wordle answers.

##### Stats

Word Bank Size: 14000<br />
Number of Test: 10000

Chance of beating Wordle (<= 6 guesses): 88.01%<br />
Average guesses: 5.52<br />
Time taken to run: 3277.33 seconds<br />

# Usage

The first 3 algorytms (Random Solver, Most Common Letter and Best Guess Unoptimized) are in the "Old Algorithm" folder. The optimized best guess algorytms is in "New Algorytm" folder.

To run or test the first 3 alogrytms, run the "main.py" folder. I would recommend using Google Colab to run the "New Agorithm".

