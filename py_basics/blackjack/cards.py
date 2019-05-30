"""
Cards module for use with blackjack game
"""

# Imports
import random
from time import sleep as t_sleep

# My Module Imports
import sys
sys.path.append("../../common")
import jupyter_helper as jh





class Card:
    """
    Class used for playing cards

    Class Attributes
    ----------------
    suits : tuple
        All valid card suits

    ranks : list
        All valid card ranks, e.g. 2 through Ace

    vals : dict
        numerical values for each card rank

    Object Attributes
    -----------------
    suit - card suit from class attribute suits
    rank - card rank from class attribute ranks

    Methods
    -------
    suit_repr()
        Unicode print representation of suit
    """

    # Class Attributes
    suits = ('spades', 'clubs', 'hearts', 'diamonds')
    ranks = [str(x) for x in range(2, 11)] + ['J', 'Q', 'K', 'A']
    vals = {'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
            'J': 10, 'Q': 10, 'K': 10, 'A': 11}

    def __init__(self, rank, suit):
        assert rank in Card.ranks
        assert suit in Card.suits
        self.rank = rank
        self.suit = suit

    def __str__(self):
        return self.rank + self.suit_repr()

    def suit_repr(self):
        if self.suit == 'spades':      return chr(0x2660)
        elif self.suit == 'clubs':     return chr(0x2663)
        elif self.suit == 'hearts':    return chr(0x2665)
        elif self.suit == 'diamonds':  return chr(0x2666)
        else: raise ValueError("Suit not recognized")


class Deck:
    """
    Class used for playing card deck

    Attributes
    ----------
    cards : list of dicts
        All X playing cards with structure {'deck': int, 'card': Card}

    Methods
    -------
    shuffle()
        shuffle the cards in the deck

    deal()
        deal a card from the top of the deck
    """
    def __init__(self, n_decks):
        self.cards = [{'deck': ix, 'card': Card(rank, suit)} for ix in range(n_decks) for suit in Card.suits for rank in Card.ranks]

    def __str__(self):
        deck_str = "Deck:"
        for card in self.cards:
            deck_str += "\n" + card.__str__()

        return deck_str

    def shuffle(self):
        print("Shuffling the Deck ", end="")
        for _ in range(5):
            t_sleep(0.5)
            print(".", end="")
            random.shuffle(self.cards)
        print("\n")

    def deal(self):
        return self.cards.pop(0)['card']


class Hand:
    """
    Class used for dealer/player hand of cards

    Methods
    -------
    add_card
    """
    def __init__(self):
        self.cards = []
        self.val = 0
        self.aces = 0
        self.status = "live"

    def add_card(self, card):
        assert type(card) == Card

        self.cards.append(card)
        self.val += Card.vals[card.rank]

        if card.rank == 'A':
            self.aces += 1
            self.adjust_for_aces()

    def adjust_for_aces(self):
        if self.val > 21 and self.aces > 0:
            self.val -= 10
            self.aces -= 1


def set_decks():
    while True:
        jh.sleep_and_clear(1)
        try:
            n_decks = int(input("How many decks would you like to play with [1-6]? "))
        except ValueError:
            print("\nC'mon man, you can only enter a number 1-6")
        else:
            if n_decks < 1 or n_decks > 6:
                print("\nC'mon man, you can only enter 1-6")
            else:
                break
    return n_decks


def display_hands(player_hands, dealer_hand, wagers, dealer_show=False):
    assert all(type(hand) is Hand for hand in player_hands)
    assert type(dealer_hand) is Hand

    if dealer_show:
        dealer_hand_str = "Dealer Hand (Total = {:d}):".format(dealer_hand.val)
        for card in dealer_hand.cards:
            dealer_hand_str += " " + card.__str__()
    else:
        dealer_hand_str = "Dealer Hand (Total = ??): XX " + dealer_hand.cards[1].__str__()

    print(dealer_hand_str)

    for ix, hand in enumerate(player_hands):

        # If Player has 'A' display both values
        if hand.val > 10 and hand.aces != 0 and not dealer_show and hand.status == 'live':
            player_hand_str = "Player Hand #{} [{}] Wager: ${:d} (Total: " \
                              "{:d} or {:d}):".format(ix + 1, hand.status, wagers[ix], hand.val - 10, hand.val)
        else:
            player_hand_str = "Player Hand #{} [{}] Wager: ${:d} (Total: " \
                              "{:d}):".format(ix + 1, hand.status, wagers[ix], hand.val)
        for card in hand.cards:
            player_hand_str += " " + card.__str__()

        print(player_hand_str)
