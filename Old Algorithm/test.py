from solver import *
import time

def test(word_list, bank_size, num_tests, algorithm):
    # word_list = set(random.sample(word_list, bank_size))
    # answers = random.sample(word_list, num_tests)
    word_list = read_word_bank('realwordbank.csv')
    answers = read_word_bank('realanswers.csv')
    print('testing...')
    beat_wordle = 0
    total_attempts = 0
    counter = 1
    attempts_dict = {}
    start_time = time.time()
    for answer in answers:
        print(f"Test #{counter} Answer: {answer}")
        if algorithm == 'random':
            attempts = random_solver(answer, word_list)
        elif algorithm == 'most_common':
            attempts = most_common_solver(answer, word_list)
            attempts_dict[attempts] = attempts_dict.get(attempts, 0) + 1
        elif algorithm == 'best_guess':
            attempts = best_guess_solver(answer, word_list)
        if attempts <= 6:
            beat_wordle += 1
        total_attempts += attempts
        counter += 1
    end_time = time.time()
    print(f'Word Bank Size: {len(word_list)}')
    print(f'Number of Tests: {len(answers)}')
    print(f'Time taken: {end_time - start_time} seconds')
    print(f'Chances of Beating Wordle: {(beat_wordle / (counter - 1)) * 100}%')
    for attempts in attempts_dict:
        print(f'Number of attempts: {attempts} Number of times: {attempts_dict[attempts]}')
        if attempts >= 10:
            print(f'Words that took {attempts} attempts: {attempts_dict[attempts]}')
    average_attempts = total_attempts / len(answers)
    print(f'Average number of attempts: {average_attempts}')