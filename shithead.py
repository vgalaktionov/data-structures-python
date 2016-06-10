
"""
This script implements a simplistic 2 player version of the card game 'Shithead'. It is simplistic
in that the computer opponent always plays a random card.
"""

import random

card_values = {2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
               'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
card_suits = ['♣', '♦', '♥', '♠']


class PlayingCard:

    def __init__(self, card_value, suit):
        self.value = card_values[card_value]
        self.suit = suit
        self.readable = str(card_value) + str(suit)

    def __str__(self):
        return self.readable

    __repr__ = __str__


class CardDeck:

    def __init__(self, shuffle=False):

        self.cards = [PlayingCard(value, suit)
                      for suit in card_suits for value in card_values]
        self.n_cards = len(self.cards)
        if shuffle:
            self.shuffle()

    def __str__(self):
        return str([str(card) for card in self.cards])

    __repr__ = __str__

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, player, hidden_cards=False, open_cards=False):
        card_dealed = self.cards[-1]
        self.cards.pop()
        if hidden_cards:
            player.hidden_cards.append(card_dealed)
        elif open_cards:
            player.open_cards.append(card_dealed)
        else:
            player.hand.append(card_dealed)

    def get_card_count(self):
        return len(self.cards)


class Player:

    def __init__(self):
        self.open_cards = []
        self.hidden_cards = []
        self.hand = []

    def __str__(self):
        return ('Hidden cards: ' + str(['[x]' for card in self.hidden_cards]) +
                '\n Open cards: ' + str(self.open_cards) +
                '\n Hand: ' + str(self.hand))

    def switch_cards(self, open_card_to_switch, hand_card_to_switch):

        self.open_cards.append(self.hand[hand_card_to_switch])
        self.hand.append(self.open_cards[open_card_to_switch])
        self.open_cards.pop(open_card_to_switch)
        self.hand.pop(hand_card_to_switch)

    def count_cards(self):
        return len(self.open_cards) + len(self.hidden_cards) + len(self.hand)

    def play_card(self, card_index, stack, hidden_cards=False, open_cards=False):

        if hidden_cards:
            card_played = self.hidden_cards[card_index]
            self.hidden_cards.pop(card_index)
        elif open_cards:
            card_played = self.open_cards[card_index]
            self.open_cards.pop(card_index)
        else:
            card_played = self.hand[card_index]
            self.hand.pop(card_index)

        stack.append(card_played)

    def check_remove_4(self):
        hand_values = [card.value for card in self.hand]
        for value in hand_values:
            if hand_values.count(value) == 4:
                to_remove = value
                for card_index, card in enumerate(self.hand):
                    if card.value == to_remove:
                        self.hand.pop(card_index)


def print_table():

    print('\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n' +
          'Opponent hidden cards: ' + str(['[x]' for card in opponent.hidden_cards]) +
          '\n Opponent open cards: ' + str(opponent.open_cards))
    print('_______________________________________\n' + str(stack))

    print('_______________________________________\n' + str(human) +
          '\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

# Main game logic starts here

deck = CardDeck(shuffle=True)
opponent = Player()
human = Player()
stack = []

for _ in range(3):
    deck.deal(opponent, hidden_cards=True)
    deck.deal(human, hidden_cards=True)

for _ in range(3):
    deck.deal(opponent, open_cards=True)
    deck.deal(human, open_cards=True)

for _ in range(3):
    deck.deal(opponent)
    deck.deal(human)

print('\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx\n' +
      str(human) +
      '\nxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

player_wants_to_switch = input('Switch cards? [y/n]')

while player_wants_to_switch == 'y':
    open_card_to_switch = int(input('Which open card to switch? [1, 2, 3]')) - 1
    hand_card_to_switch = int(input('Which hand card to switch? [1, 2, 3]')) - 1

    human.switch_cards(open_card_to_switch, hand_card_to_switch)
    print(human)
    player_wants_to_switch = input('Switch cards? [y/n] ')

opponent.play_card(random.randint(0, len(opponent.hand) - 1), stack)

while human.count_cards() > 0 and opponent.count_cards() > 0:

    print('You are up: ')
    human.check_remove_4()

    if len(human.hand) > 0:
        while len(human.hand) < 3 and len(deck.cards) > 0:
            deck.deal(human)
        print_table()
        card_to_play = int(input('Hand card to play? ' +
                                 str([x for x in range(len(human.hand) + 1)]) + ' ')) - 1
        if card_to_play >= 0:
            human.play_card(card_to_play, stack)
            if len(stack) > 1 and stack[-1].value < stack[-2].value:
                print('You took the stack.')
                human.hand.extend(stack)
                stack = []
        else:
            print('You took the stack.')
            human.hand.extend(stack)
            stack = []

    elif len(human.open_cards) > 0:
        print_table()
        card_to_play = int(input('Open card to play? ' +
                                 str([x for x in range(len(human.open_cards) + 1)]) + ' ')) - 1
        if card_to_play >= 0:
            human.play_card(card_to_play, stack, open_cards=True)
            if len(stack) > 1 and stack[-1].value < stack[-2].value:
                print('You took the stack.')
                human.open_cards.extend(stack[-1])
                human.hand.extend(stack[0:-1])
                stack = []
        else:
            print('You took the stack.')
            human.hand.extend(stack)
            stack = []

    else:
        print_table()
        card_to_play = int(input('Hidden card to play? ' +
                                 str([x for x in range(len(human.hidden_cards) + 1)]) + ' ')) - 1
        if card_to_play >= 0:
            human.play_card(card_to_play, stack, hidden_cards=True)
            if len(stack) > 1 and stack[-1].value < stack[-2].value:
                print('You took the stack.')
                human.hand.extend(stack)
                stack = []
        else:
            print('You took the stack.')
            human.hand.extend(stack)
            stack = []

    print_table()
    print('Opponent is up: ')
    opponent.check_remove_4()

    if len(opponent.hand) > 0:
        while len(opponent.hand) < 3 and len(deck.cards) > 0:
            deck.deal(opponent)
        opponent.play_card(random.randint(0, len(opponent.hand) - 1), stack)
        if len(stack) > 1 and stack[-1].value < stack[-2].value:
            print('Opponent took the stack.')
            opponent.hand.extend(stack)
            stack = []

    elif len(opponent.open_cards) > 0:
        print_table()
        opponent.play_card(random.randint(0, len(opponent.open_cards) - 1), stack)
        if len(stack) > 1 and stack[-1].value < stack[-2].value:
            print('Opponent took the stack.')
            opponent.open_cards.extend(stack[-1])
            opponent.hand.extend(stack[0:-1])
            stack = []

    else:
        print_table()
        opponent.play_card(random.randint(0, len(opponent.hidden_cards) - 1), stack)
        if len(stack) > 1 and stack[-1].value < stack[-2].value:
            print('Opponent took the stack.')
            opponent.hand.extend(stack)
            stack = []


if human.count_cards() == 0:
    print('You win!')
else:
    print('Computer wins!')
