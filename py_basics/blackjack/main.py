"""
This is the main script to run the blackjack game
"""

__author__ = "Mitch Frankel"
__version__ = "0.0.0"

# TODO: docstrings

# My Module Imports
import sys
sys.path.append("../../..")
from common import jupyter_helper as jh
from cards import *

# Globals
global chip_stack
chip_stack = ChipStack()

class ChipStack:
    def __init__(self):
        self.val = None
        self.bets = [None]
        self.insurance = 'n'

    def win_bet(self, bet_ix):
        self.val += self.bets[bet_ix]

    def lose_bet(self, bet_ix):
        self.val -= self.bets[bet_ix]

    def split_bet(self):
        self.bets.append(self.bets[-1])

    def win_blackjack(self):
        self.val += int(self.bets[0] * 1.5)

    def set_insurance(self):
        while True:
            self.insurance = input("Do you want insurance? Enter amount or [n]: ")
            if self.insurance == 'n':
                break
            else:
                try:
                    self.insurance = int(self.insurance)
                    if self.insurance > self.val - self.bets[0]:
                        print("You cannot wager more than you have {}".format(self.val - self.bets[0]))
                    elif self.insurance < 0:
                        print("Wager must be greater than 0")
                    else:
                        break
                except ValueError:
                    print("Wager must be whole number greater than 0")

    def win_insurance(self):
        print("Player Wins Insurance Bet")
        self.val += self.insurance

    def lose_insurance(self):
        print("No Dealer BlackJack, Player Loses Insurance Bet")
        self.val -= self.insurance

    def init_stack(self):
        while True:
            try:
                self.val = int(input("How many chips would you like to start with? "))
            except ValueError:
                print("You must enter a whole number")
                jh.sleep_and_clear(1)
            else:
                if self.val < 0:
                    print("You must enter a number greater than 0")
                    jh.sleep_and_clear(1)
                else:
                    break

    def take_bet(self):
        while True:
            self.bets[0] = input("Chip Stack = ${}, How much would you like to "
                                 "wager [x to exit]? ".format(self.val))
            if self.bets[0] == 'x':
                return "exit"

            try:
                self.bets[0] = int(self.bets[0])
            except ValueError:
                print("\nC'mon man, You must enter a whole number")
                jh.sleep_and_clear(1)
            else:
                if self.bets[0] > self.val:
                    print("\nC'mon man, You cannot wager more than your current stack of ${}".format(self.val))
                    jh.sleep_and_clear(1)
                elif self.bets[0] < 0:
                    print("\nC'mon man, You must enter a value greater than 0")
                    jh.sleep_and_clear(1)
                else:
                    jh.sleep_and_clear(1)
                    print("Wager is ${}".format(self.bets[0]))
                    break
        return "wager"


def hit(deck: Deck, hand: Hand):

    assert type(deck) is Deck
    assert type(hand) is Hand

    hand.add_card(deck.deal())
    hand.adjust_for_aces()
    return hand


def hit_stand_double(deck, player_hands, dealer_hand, hand_ix):

    global chip_stack

    double_down_ask = True

    while True:
        while True:
            print("Wager is ${}".format(chip_stack.bets[hand_ix]))
            if double_down_ask:
                hit_stand = input("Player Hand #{}: Do you want to double down [d], "
                                  "hit [h], or stand [s]? ".format(hand_ix + 1))
                double_down_ask = False
            else:
                hit_stand = input("Player Hand #{}: Do you want to hit [h], or stand [s]? ".format(hand_ix + 1))

            if hit_stand.lower() not in "hds":
                print("\nC'mon man, that ain't a valid response!")
            else:
                break

        if hit_stand.lower() == 's':
            print("Player Stands")
            status = 'ongoing'
            break

        else:
            if hit_stand.lower() == 'd':
                print("Player Double Downs, gets one card")
                chip_stack.bets[hand_ix] *= 2
            else:
                print("Player Hits")

            jh.sleep_and_clear(1)
            player_hands[hand_ix] = hit(deck, player_hands[hand_ix])
            display_hands(player_hands, dealer_hand, dealer_show=False)

            if player_hands[hand_ix].val > 21:
                print("Player has busted, womp womp")
                chip_stack.lose_bet(hand_ix)
                status = 'loser'
                break
            else:
                if hit_stand.lower() == 'd':
                    status = 'ongoing'
                    break

    return status


def check_dealer_blackjack(player_hands, dealer_hand):

    global chip_stack

    if dealer_hand.cards[1].rank == 'A':
        chip_stack.set_insurance()

    # If Dealer Has 21, player loses bet
    if dealer_hand.val == 21:
        display_hands(player_hands, dealer_hand, dealer_show=True)
        print("Dealer Has Blackjack, Player Loses")
        chip_stack.lose_bet(0)

        # Check for A and insurance (win insurance)
        if dealer_hand.cards[1].rank == 'A' and chip_stack.insurance != 'n':
            chip_stack.win_insurance()

        return "loser"

    # If no 21, check for A and insurance (lose insurance)
    else:
        if dealer_hand.cards[1].rank == 'A':
            if chip_stack.insurance != 'n':
                chip_stack.lose_insurance()
            else:
                print("No Dealer Blackjack")
        return "ongoing"


def check_for_splits(deck, player_hands, dealer_hand, hand_ix):

    global chip_stack

    if player_hands[hand_ix].cards[0].rank == player_hands[hand_ix].cards[1].rank:
        if input("Player Hand #{}: Do you want to split the hand [y/n]? ".format(hand_ix+1)).lower() == 'y':
            player_hands.append(Hand())
            player_hands[-1].add_card(player_hands[hand_ix].cards.pop())
            player_hands[hand_ix].val -= Card.vals[player_hands[-1].cards[0].rank]
            player_hands[hand_ix].add_card(deck.deal())
            player_hands[-1].add_card(deck.deal())
            jh.sleep_and_clear(1)
            display_hands(player_hands, dealer_hand, dealer_show=False)
            chip_stack.split_bet()


def run_game():

    # Initialize game
    print("Welcome to Blackjack!")
    print("Here are the Rules:")
    print("1) Dealer must hit below 17 and must stand on soft 17")
    print("2) Blackjack pays 1.5x")
    print("3) Double downs are accepted")
    print("4) Blackjack and Double Downs work on split hands")
    _ = input("\nReady Player? [y] ")

    # Set n_decks
    n_decks = set_decks()

    # Initialize player chip sta
    chip_stack.init_stack()

    # Initialize Deck
    deck = Deck(n_decks)
    deck.shuffle()
    deck_cut = deck.cards[int(len(deck.cards) * 2/3):]

    while True:

        # Check for deck cut status and reset deck if needed
        if deck.cards[0] in deck_cut:
            jh.clear_display()
            print("Time for a new deck!")
            deck = Deck(n_decks)
            deck.shuffle()
            jh.clear_display()

        # Take Bet or exit
        if chip_stack.take_bet() == "exit":
            break

        # Set Player Hand
        player_hands = [Hand()]
        player_hands[0].add_card(deck.deal())
        player_hands[0].add_card(deck.deal())

        # Set Dealer Hand
        dealer_hand = Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Display hand w/dealer card hidden
        display_hands(player_hands, dealer_hand, dealer_show=False)

        # Check for dealer blackjack
        status = check_dealer_blackjack(player_hands, dealer_hand)
        if status == 'loser':
            jh.sleep_and_clear(1)
            continue

        # Loop through all player hands and play player hands
        player_hand_ix = 0
        status = ["loser"]

        while True:

            # Check for player blackjack
            if player_hands[-1].val == 21:
                print("BLACKJACK! Player wins ${}".format(int(chip_stack.bets[-1] * 1.5)))
                chip_stack.win_blackjack()
                break

            # Check for split
            check_for_splits(deck, player_hands, dealer_hand, player_hand_ix)

            # Ask player hit or stand?
            status[-1] = hit_stand_double(deck, player_hands, dealer_hand, player_hand_ix)

            player_hand_ix += 1
            status.append("loser")
            if player_hand_ix == len(player_hands):
                break
            else:
                jh.sleep_and_clear(1)
                display_hands(player_hands, dealer_hand, dealer_show=False)

        # If player has blackjack in all hands, continue
        for hand in player_hands:
            if not(hand.val == 21 and len(hand.cards) == 2):
                all_bj = False
                break
        else:
            all_bj = True

        if all_bj: continue

        # If all players are not busted, display dealer hand and play dealer hand
        if not all(x == "loser" for x in status):
            jh.sleep_and_clear(1)
            display_hands(player_hands, dealer_hand, dealer_show=True)

            # Dealer Must Hit Below 17
            while dealer_hand.val < 17:
                print("Dealer Has {}, Must Hit".format(dealer_hand.val))
                jh.sleep_and_clear(1.5)
                dealer_hand = hit(deck, dealer_hand)
                dealer_hand.adjust_for_aces()
                display_hands(player_hands, dealer_hand, dealer_show=True)

            # Check dealer against all hands
            for hand_ix in range(len(player_hands)):

                # Check dealer value against player
                if dealer_hand.val > 21:
                    print("Player Hand #{}: Dealer Has Busted, Player Wins".format(hand_ix+1))
                    chip_stack.win_bet(hand_ix)
                elif dealer_hand.val == player_hands[hand_ix].val:
                    print("Player Hand #{}: Push, no glory for either side".format(hand_ix+1))
                elif dealer_hand.val < player_hands[hand_ix].val:
                    print("Player Hand #{}: Dealer Has {}, Player Has {}, "
                          "Player Wins!".format(hand_ix+1, dealer_hand.val, player_hands[hand_ix].val))
                    chip_stack.win_bet(hand_ix)
                else:
                    print("Player Hand #{}: Dealer Has {}, Player Has {}, "
                          "Player Loses".format(hand_ix+1, dealer_hand.val, player_hands[hand_ix].val))
                    chip_stack.lose_bet(hand_ix)

    # End of game
    jh.sleep_and_clear(1)
    print("Sorry to see you go, but I'll enjoy watching you walkaway")


if __name__ == "__main__":
    run_game()
