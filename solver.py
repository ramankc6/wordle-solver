import random
from collections import Counter

# Make a list of words from the wordbank
def read_word_list(filename):
    words = {}
    with open(filename, 'r') as file:
        words = {line.strip().lower() for line in file if len(line.strip()) == 5}
    return words


#Find the letters that match the guess
def grade_guess(answer, guess):
    green = 0
    yellow = 0
    for i in range(len(answer)):
        if answer[i] == guess[i]:
            green += 1
        elif guess[i] in answer:
            yellow += 1
    return green, yellow

#Solve using random guess
def random_solver (answer, word_list):
    # print('Random Guesser')
    remaining_words = word_list.copy()
    attempts = 0

    while remaining_words:
        guess = random.choice(remaining_words)
        attempts += 1
        # print(f'Guess {attempts}: {guess}')

        green, yellow = grade_guess(answer, guess)
        if green == 5:
            # print(f'Guessed {guess} in {attempts} attempts')
            break
        remaining_words = [word for word in remaining_words if grade_guess(word, guess) == (green, yellow)]
    return attempts


#Solve using most common letter guess
def most_common_letters(word_list, count):
    letter_counts = Counter(''.join(word_list))
    return [item[0] for item in letter_counts.most_common(count)]

def most_common_solver(answer, word_list):
    # print('Most Common Guesser')
    remaining_words = word_list.copy()
    attempts = 0

    while remaining_words:
        common_letters = ''.join(most_common_letters(remaining_words, 5))
        guess = random.choice([word for word in remaining_words if set(word) & set(common_letters)])
        attempts += 1
        # print(f'Guess {attempts}: {guess}')

        green, yellow = grade_guess(answer, guess)
        if green == 5:
            # print(f'Guessed {guess} in {attempts} attempts')
            break
        remaining_words = [word for word in remaining_words if grade_guess(word, guess) == (green, yellow)]
    return attempts

#Solve using best possible guess
def best_guess(word_list, all_combinations):
    min_max_score = float("inf")
    best_guess = None

    for candidate in all_combinations:
        scores = {}
        for word in word_list:
            score = grade_guess(candidate, word)
            scores[score] = scores.get(score, 0) + 1
    
        max_score = max(scores.values())
        if max_score < min_max_score:
            min_max_score = max_score
            best_guess = candidate
    return best_guess

def best_guess_solver(answer, word_list):
    print('Best Guess Guesser')
    remaining_words = word_list.copy()
    all_combinations = word_list.copy()
    attempts = 0

    while remaining_words:
        guess = best_guess(remaining_words, all_combinations) if attempts > 0 else random.choice(list(remaining_words)) # Salet is the first guess. It is statistically the best guess for the first guess
        attempts += 1
        print(f'Guess {attempts}: {guess}')

        green, yellow = grade_guess(answer, guess)
        if green == 5:
            print(f'Guessed {guess} in {attempts} attempts')
            break
        remaining_words = {word for word in remaining_words if grade_guess(guess, word) == (green, yellow)}
        all_combinations.discard(guess)
    return attempts

#Finds the average number of attempts for a given algorithm after 1000 trials
def tester(answer, word_list, algorithm):
    total_score = 0
    if algorithm == 'random':
        for i in range(1000):
            total_score = total_score + random_solver(answer, word_list)
        average_score = total_score / 1000
    elif algorithm == 'most_common':
        for i in range(1000):
            total_score = total_score + most_common_solver(answer, word_list)
        average_score = total_score / 1000
    return average_score



def main():
    word_list = read_word_list('wordbank.csv')
    answer = 'apple'
    # random_solver(answer, word_list)
    # most_common_solver(answer, word_list)
    best_guess_solver(answer, word_list)
    # print(tester (answer, word_list, 'random'))
    # print(tester (answer, word_list, 'most_common'))
main()