import math
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
    green_location = []
    yellow_location = []

    for i in range(len(answer)):
        if answer[i] == guess[i]:
            green += 1
            green_letters.append(answer[i])
            green_location.append((answer[i], i))
            unmatched_answer.discard(answer[i])
            unmatched_guess.discard(guess[i])
        if guess[i] in set(answer):
            yellow += 1
            if guess[i] != answer[i]:
              yellow_location.append((guess[i], i))

    yellow_letters = list(unmatched_answer & unmatched_guess)
    yellow = len(yellow_letters)
    grade_guess_cache[(answer, guess)] = (green, yellow, set(green_letters), set(yellow_letters), set(green_location), set(yellow_location))
    return green, yellow, set(green_letters), set(yellow_letters), set(green_location), set(yellow_location)


@lru_cache(maxsize=None)
def entropy(word_list):
    count = len(word_list)
    if count == 0:
        return 0
    probability = 1 / count
    return -sum(probability * math.log2(probability) for _ in word_list)



def conditional_entropy(word_list, candidate, all_cbinations):
    scores = defaultdict(list)

    for word in word_list:
        score = grade_guess(candidate, word)
        score_tuple = score[0], score[1], tuple(sorted(score[2])), tuple(sorted(score[3]))
        scores[score_tuple].append(word)

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


def most_common_letters(word_list, count):
    letter_counts = Counter(''.join(word_list))
    return [item[0] for item in letter_counts.most_common(count)]



def best_guess_func(word_list, all_combinations):
    current_entropy = entropy(tuple(word_list))

    sorted_combinations = sorted(all_combinations, key=lambda word: sum(Counter(word_list).get(letter, 0) for letter in word), reverse=True)

    max_information_gain = float('-inf')
    best_guess = None

    for idx, candidate in enumerate(sorted_combinations):
        info_gain = parallel_information_gain((word_list, candidate, all_combinations, current_entropy))
        if info_gain > max_information_gain:
            max_information_gain = info_gain
            best_guess = candidate
        if max_information_gain >= 0.99 * current_entropy:
            break
    if best_guess not in read_word_bank('realanswers.csv'):
        word_list.remove(best_guess)
        best_guess = best_guess_func(word_list, all_combinations)
    return best_guess


def best_guess_solver(answer, word_list):
    remaining_words = word_list.copy()
    attempts = 0
    green_letters = {}
    yellow_letters = {}
    green = 0
    yellow = 0

    while remaining_words:
      if attempts == 0:
          guess = 'salet'
      # elif attempts == 1:
      #     guess = 'crony'
      elif attempts == 1:
          common_letters = ''.join(remaining_words)
          for letter in green_letters:
              common_letters.replace(letter, '')
          for letter in yellow_letters:
              common_letters.replace(letter, '')
          common_letters = set(most_common_letters(remaining_words, 9))
          for letter in green_letters:
              common_letters.discard(letter)
          for letter in yellow_letters:
              common_letters.discard(letter)
          # print(common_letters)
          word_scores = [(word, len(set(word) & set(common_letters))) for word in read_word_bank('realwordbank.csv')]
          word_scores_sorted = sorted(word_scores, key=lambda x: x[1], reverse=True)
          
          max_score = word_scores_sorted[0][1]
          top_words = [word for word, score in word_scores_sorted if score == max_score]

          min_entropy = float('inf')
          best_entropy_word = None
          for word in top_words:
              word_entropy = entropy(tuple(word))
              if word_entropy < min_entropy:
                  min_entropy = word_entropy
                  best_entropy_word = word
          guess = best_entropy_word
      else:
          guess = best_guess_func(remaining_words, remaining_words)
      attempts += 1
      print(f'Guess {attempts}: {guess}')
      green, yellow, green_letters, yellow_letters, green_location, yellow_location = grade_guess(answer, guess)
      
      if green == 5:
          break

      remaining_words = {word for word in remaining_words if grade_guess(guess, word)[:-1] == (green, yellow, green_letters, yellow_letters, green_location)}

      for letters in yellow_location:
        for word in remaining_words:
          if (word[letters[1]] == letters[0]):
            remaining_words.remove(word)
      remaining_words.discard('salet')

    return attempts


def test(word_list, bank_size, num_tests):
    word_list = set(word_list)
    answers = read_word_bank('realanswers.csv')
    # answers = {'apple'}
    print('testing...')
    beat_wordle = 0
    total_attempts = 0
    counter = 1
    lost_list = []
    for answer in answers:
        print(f"Test #{counter} Answer: {answer}")
        attempts = best_guess_solver(answer, word_list)
        if attempts <= 6:
            beat_wordle += 1
        else:
          lost_list.append(answer)
        total_attempts += attempts
        counter += 1
    print(f'Chances of Beating Wordle: {(beat_wordle / (counter - 1)) * 100}%')
    average_attempts = total_attempts / len(answers)
    print(f'Average number of attempts: {average_attempts}')
    print(lost_list)


def main():
    start_time = time.time()
    word_list = read_word_bank('realwordbank.csv')
    bank_size = 14000
    num_tests = 2
    test(word_list, bank_size, num_tests)
    end_time = time.time()
    print(f'Time taken: {end_time - start_time} seconds')

main()