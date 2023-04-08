import math
import random
import time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
from functools import lru_cache
from collections import defaultdict

grade_guess_cache = {}
entropy_cache = {}


def read_word_bank(filename):
    words = {}
    with open(filename, 'r') as file:
        words = {line.strip().lower() for line in file if len(line.strip()) == 5}

    return words


def grade_guess(answer, guess):
    if (answer, guess) in grade_guess_cache:
        return grade_guess_cache[(answer, guess)]
    green = 0
    yellow = 0
    unmatched_answer = set(answer)
    unmatched_guess = set(guess)
    yellow_letters = []
    green_letters = []

    for i in range(len(answer)):
        if answer[i] == guess[i]:
            green += 1
            green_letters.append(answer[i])
            unmatched_answer.discard(answer[i])
            unmatched_guess.discard(guess[i])

    yellow_letters = list(unmatched_answer & unmatched_guess)
    yellow = len(yellow_letters)

    grade_guess_cache[(answer, guess)] = (green, yellow, set(green_letters), set(yellow_letters))
    return green, yellow, set(green_letters), set(yellow_letters)


@lru_cache(maxsize=None)
def entropy(word_list):
    count = len(word_list)
    probability = 1 / count
    return -sum(probability * math.log2(probability) for _ in word_list)


def conditional_entropy(word_list, candidate, all_cbinations):
    scores = defaultdict(list)

    for word in word_list:
        score = grade_guess(candidate, word)
        score = score[0],score[1]
        scores[score].append(word)

    total_entropy = 0
    for score, words in scores.items():
        if words:
            score_probability = len(words) / len(word_list)
            total_entropy += score_probability * entropy(tuple(words))
    return total_entropy


def parallel_information_gain(args):
    word_list, candidate, all_combinations, current_entropy = args
    cond_entropy = conditional_entropy(word_list, candidate, all_combinations)
    return current_entropy - cond_entropy


def most_common_letters(word_list, n):
    letter_count = Counter(letter for word in word_list for letter in word)
    return set(letter for letter, _ in letter_count.most_common(n))


def best_guess(word_list, all_combinations):
    current_entropy = entropy(tuple(word_list))

    sorted_combinations = sorted(all_combinations, key=lambda word: sum(Counter(word_list).get(letter, 0) for letter in word), reverse=True)

    max_information_gain = float('-inf')
    best_guess = None

    with ProcessPoolExecutor() as executor:
        for idx, candidate in enumerate(sorted_combinations):
            info_gain = parallel_information_gain((word_list, candidate, all_combinations, current_entropy))
            if info_gain > max_information_gain:
                max_information_gain = info_gain
                best_guess = candidate
            # progress = (idx + 1) / len(sorted_combinations) * 100
            # print(f"Progress: {progress:.2f}%")
            if max_information_gain >= 0.99 * current_entropy:
                break

    return best_guess


def best_guess_solver(answer, word_list):
    print('Best Guess Guesser')
    remaining_words = word_list.copy()
    attempts = 0
    green_letters = {}
    yellow_letters = {}
    green = 0
    yellow = 0

    while remaining_words:
        guess = best_guess(remaining_words, remaining_words) if attempts > 0 else "slate"
        attempts += 1
        print(f'Guess {attempts}: {guess}')

        green, yellow, green_letters, yellow_letters = grade_guess(answer, guess)
        if green == 5:
            print(f'Guessed {guess} in {attempts} attempts')
            break
        remaining_words = {word for word in remaining_words if grade_guess(guess, word) == (green, yellow, green_letters, yellow_letters)}
    return attempts


def test(word_list, bank_size, num_tests):
    word_list = set(word_list)
    answers = read_word_bank('realanswers.csv')
    print('testing...')
    beat_wordle = 0
    total_attempts = 0
    counter = 1
    for answer in answers:
        print(f"Test #{counter} Answer: {answer}")
        attempts = best_guess_solver(answer, word_list)
        if attempts <= 6:
            beat_wordle += 1
        total_attempts += attempts
        counter += 1
    print(f'Chances of Beating Wordle: {(beat_wordle / (counter - 1)) * 100}%')
    average_attempts = total_attempts / len(answers)
    print(f'Average number of attempts: {average_attempts}')


def main():
    start_time = time.time()
    word_list = read_word_bank('realwordbank.csv')
    bank_size = 14000
    num_tests = 2
    test(word_list, bank_size, num_tests)
    end_time = time.time()
    print(f'Time taken: {end_time - start_time} seconds')


main()