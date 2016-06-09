import random

target_string = 'methinks it is like a weasel'


def monkey_typewriter():
    alphabet = 'abcdefghijklmnopqrstuvwxyz '
    sentence = ''
    for i in range(0, 26):
        sentence += alphabet[random.randint(0, 26)]
    return sentence


def scorer(sentence):
    target_string = 'methinks it is like a weasel'
    score = 0
    for index, letter in enumerate(sentence):
        if letter == target_string[index]:
            score += 1
    return score


def looper():
    attempts = 0
    high_score = 0
    while True:
        sentence = monkey_typewriter()
        score = scorer(sentence)
        attempts += 1
        if score == 27:
            print('Success after {} attempts'.format(attempts))
            break
        if score > high_score:
            high_score = score
            best_attempt = sentence
        if attempts % 100000 == 0:
            print('Best attempt : "{}", score: {}'.format(
                best_attempt, high_score))
