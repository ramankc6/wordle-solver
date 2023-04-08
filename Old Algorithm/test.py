from solver import *

def test(word_list, bank_size, num_tests, algorithm):
    word_list = set(random.sample(word_list, bank_size))
    answers = random.sample(word_list, num_tests)
    print('testing...')
    beat_wordle = 0
    total_attempts = 0
    counter = 1
    for answer in answers:
        print(f"Test #{counter} Answer: {answer}")
        if algorithm == 'random':
            attempts = random_solver(answer, word_list)
        elif algorithm == 'most_common':
            attempts = most_common_solver(answer, word_list)
        elif algorithm == 'best_guess':
            attempts = best_guess_solver(answer, word_list)
        if attempts <= 5:
            beat_wordle += 1
        total_attempts += attempts
        counter += 1
    print(f'Chances of Beating Wordle: {(beat_wordle / (counter - 1)) * 100}%')
    average_attempts = total_attempts / len(answers)
    print(f'Average number of attempts: {average_attempts}')