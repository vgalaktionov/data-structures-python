import random

alphabet = 'abcdefghijklmnopqrstuvwxyz '
target_string = 'methinks it is like a weasel'


def monkey_initial():
    sentence = ''
    for i in range(0, 28):
        sentence += alphabet[random.randint(0, 26)]
    return sentence


def monkey_improve(sentence):
    sentence = list(sentence)
    for index, letter in enumerate(sentence):
        if letter != target_string[index]:
            sentence[index] = alphabet[random.randint(0, 26)]
            break
    sentence = ''.join(sentence)
    return sentence


def scorer(sentence):
    score = 0
    for index, letter in enumerate(sentence):
        if letter == target_string[index]:
            score += 1
    return score


def looper():

    attempts = 0
    high_score = 0
    sentence = monkey_initial()
    best_attempt = ""
    while True:
        score = scorer(sentence)

        if score == 28:
            print('Success after {} attempts'.format(attempts))
            break

        if score > high_score:
            high_score = score
            best_attempt = sentence

        attempts += 1

        if attempts % 1000 == 0:
            print('Best attempt : "{}", score: {}'.format(
                best_attempt, high_score))

        sentence = monkey_improve(sentence)
