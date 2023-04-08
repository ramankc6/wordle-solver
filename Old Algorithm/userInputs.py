from solver import *
from test import *

def get_user_input(file):

    word_list = read_word_bank(file)

    print('Welcome to the Wordle Solver!')
    print('Please slect a function:')
    print('1. Solve for Word')
    print('2. Run Tests')

    choice = int(input('Enter your choice: '))

    if choice == 1:
        print('Slect Algorithm:')
        print('1. Random Guess (Fastest)')
        print('2. Most Common Letter Guess')
        print('3. Best Guess Algorithm (Most Accurate)')
        algorithm = int(input('Enter your choice: '))
        if algorithm == 1:
            print('Random Guess')
            answer = input('Enter the word: ')
            attempts = random_solver(answer, word_list)
            print(f'Guessed {answer} in {attempts} attempts')
        elif algorithm == 2:
            print('Most Common Letter Guess')
            answer = input('Enter the word: ')
            attempts = most_common_solver(answer, word_list)
            print(f'Guessed {answer} in {attempts} attempts')
        elif algorithm == 3:
            print('Best Guess Algorithm')
            answer = input('Enter the word: ')
            attempts = best_guess_solver(answer, word_list)
            print(f'Guessed {answer} in {attempts} attempts')
    elif choice == 2:
        bank_size = int(input('Enter the size of the word bank: '))
        num_tests = int(input('Enter the number of tests to run: '))
        print('Slect Algorithm:')
        print('1. Random Guess (Fastest)')
        print('2. Most Common Letter Guess')
        print('3. Best Guess Algorithm (Most Accurate)')
        algorithm = int(input('Enter your choice: '))
        if algorithm == 1:
            test(word_list, bank_size, num_tests, 'random')
        elif algorithm == 2:
            test(word_list, bank_size, num_tests, 'most_common')
        elif algorithm == 3:
            test(word_list, bank_size, num_tests, 'best_guess')