"""
This is the main script to run the blackjack game
"""

__author__ = "Mitch Frankel"
__version__ = "0.0.0"

# TODO: docstrings

# My Module Imports
import sys
sys.path.append("../../common")
import jupyter_helper as jh
import cards


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
        print("Player Wins ${} Insurance Bet".format(self.insurance))
        self.val += self.insurance

    def lose_insurance(self):
        print("No Dealer BlackJack, Player Loses ${} Insurance Bet".format(self.insurance))
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
            self.bets = [input("Chip Stack = ${}, How much would you like to "
                               "wager [x to exit]? ".format(self.val, self.bets[0]))]
            if self.bets[0] == 'x':
                return "exit"
            else:
                try:
                    self.bets[0] = int(self.bets[0])
                except ValueError:
                    print("\nC'mon man, You must enter a whole number")
                    jh.sleep_and_clear(1)
                else:
                    if self.bets[0] > self.val:
                        print("\nC'mon man, You cannot wager more than your current stack of ${}".format(self.val))
                        jh.sleep_and_clear(1)
                    elif self.bets[0] < 1:
                        print("\nC'mon man, You must enter a value greater than 0")
                        jh.sleep_and_clear(1)
                    else:
                        jh.sleep_and_clear(1)
                        break
        return "wager"


def hit(deck: cards.Deck, hand: cards.Hand):

    assert type(deck) is cards.Deck
    assert type(hand) is cards.Hand

    hand.add_card(deck.deal())
    hand.adjust_for_aces()
    return hand


def hit_stand_double(deck, dealer_hand, hand_ix):

    global chip_stack, player_hands

    double_down_ask = True

    while True:
        while True:
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
            player_hands[hand_ix].status = 'live-stand'
            break

        else:
            if hit_stand.lower() == 'd':
                print("Player Double Downs, gets one card")
                chip_stack.bets[hand_ix] *= 2
            else:
                print("Player Hits")

            jh.sleep_and_clear(1)
            player_hands[hand_ix] = hit(deck, player_hands[hand_ix])
            cards.display_hands(player_hands, dealer_hand, chip_stack.bets, dealer_show=False)

            if player_hands[hand_ix].val > 21:
                print("Player has busted, Player Loses Wager")
                chip_stack.lose_bet(hand_ix)
                player_hands[hand_ix].status = 'bust'
                break
            else:
                if hit_stand.lower() == 'd':
                    player_hands[hand_ix].status = 'live-doubledown'
                    break


def check_dealer_blackjack(dealer_hand):

    global chip_stack, player_hands

    if dealer_hand.cards[1].rank == 'A':
        chip_stack.set_insurance()

    # If Dealer Has 21, player loses bet unless player has blackjack as well
    if dealer_hand.val == 21:
        jh.sleep_and_clear(1)
        cards.display_hands(player_hands, dealer_hand, chip_stack.bets, dealer_show=True)

        if player_hands[0].val == 21:
            print("Dealer Has Blackjack, Player Hand is a Push")
        else:
            print("Dealer Has Blackjack, Player Loses Wager")
            chip_stack.lose_bet(0)

        # Check for A and insurance (win insurance)
        if dealer_hand.cards[1].rank == 'A' and chip_stack.insurance != 'n':
            chip_stack.win_insurance()

        player_hands[-1].status = 'dealer blackjack'

    # If no 21, check for A and insurance (lose insurance)
    else:
        if dealer_hand.cards[1].rank == 'A':
            if chip_stack.insurance != 'n':
                chip_stack.lose_insurance()
            else:
                print("No Dealer Blackjack")


def check_for_splits(deck, dealer_hand, hand_ix):

    global chip_stack, player_hands

    while player_hands[hand_ix].cards[0].rank == player_hands[hand_ix].cards[1].rank:
        if input("Player Hand #{}: Do you want to split the hand [y/n]? ".format(hand_ix+1)).lower() == 'y':

            # Split the bet
            chip_stack.split_bet()

            # Create new hand, add card from current hand
            player_hands.append(cards.Hand())
            player_hands[-1].add_card(player_hands[hand_ix].cards.pop())
            player_hands[-1].add_card(deck.deal())

            # For current hand, remove dropped card value (accounting for aces), and add new card
            if player_hands[-1].cards[0].rank == 'A':
                player_hands[hand_ix].val = 11
                player_hands[hand_ix].aces = 1
            else:
                player_hands[hand_ix].val -= cards.Card.vals[player_hands[-1].cards[0].rank]

            player_hands[hand_ix].add_card(deck.deal())

            jh.sleep_and_clear(1)
            cards.display_hands(player_hands, dealer_hand, chip_stack.bets, dealer_show=False)


def run_game():

    # Initialize game
    print("Welcome to Blackjack!")
    print("Here are the Rules:")
    print("1) Dealer must hit below 17 and must stand on soft 17")
    print("2) Blackjack pays 1.5x")
    print("3) Double downs are accepted, player receives only 1 card")
    print("4) Blackjack and Double Downs work on split hands")
    input("\nReady Player? [y] ")
    jh.sleep_and_clear(1)

    # Set n_decks
    n_decks = cards.set_decks()
    jh.sleep_and_clear(1)

    # Initialize player chip stack
    global chip_stack
    chip_stack = ChipStack()
    chip_stack.init_stack()
    jh.sleep_and_clear(1)

    # Initialize Deck
    deck = cards.Deck(n_decks)
    deck.shuffle()
    deck_cut = deck.cards[int(len(deck.cards) * 2/3):]
    jh.sleep_and_clear(1)

    while True:

        # Check for deck cut status and reset deck if needed
        if deck.cards[0] in deck_cut:
            jh.clear_display()
            print("Time for a new deck!")
            deck = cards.Deck(n_decks)
            deck.shuffle()
            jh.clear_display()

        # Take Bet or exit
        if chip_stack.take_bet() == "exit":
            break

        # Set Player Hand
        global player_hands
        player_hands = [cards.Hand()]
        player_hands[0].add_card(deck.deal())
        player_hands[0].add_card(deck.deal())

        # Set Dealer Hand
        dealer_hand = cards.Hand()
        dealer_hand.add_card(deck.deal())
        dealer_hand.add_card(deck.deal())

        # Display hand w/dealer card hidden
        cards.display_hands(player_hands, dealer_hand, chip_stack.bets, dealer_show=False)

        # Check for dealer blackjack
        check_dealer_blackjack(dealer_hand)
        if player_hands[-1].status == 'dealer blackjack':
            jh.sleep_and_clear(1)
            continue

        # Loop through all player hands and play player hands
        player_hand_ix = 0
        while True:

            # Check for split
            check_for_splits(deck, dealer_hand, player_hand_ix)

            # Check for player blackjack
            if player_hands[player_hand_ix].val == 21:
                chip_stack.bets[player_hand_ix] = int(chip_stack.bets[player_hand_ix] * 1.5)
                print("Player Hand #{} BLACKJACK! Player wins ${}".format(player_hand_ix+1,
                                                                          chip_stack.bets[player_hand_ix]))
                chip_stack.win_bet(player_hand_ix)
                player_hands[player_hand_ix].status = 'blackjack'

            else:
                # Ask player hit or stand?
                hit_stand_double(deck, dealer_hand, player_hand_ix)

            # See if new loop needed for split
            player_hand_ix += 1
            if player_hand_ix == len(player_hands):
                break
            else:
                jh.sleep_and_clear(1)
                cards.display_hands(player_hands, dealer_hand, chip_stack.bets, dealer_show=False)

        # If player has blackjack in all hands, continue
        if all(hand.status == 'blackjack' for hand in player_hands):
            continue

        # If any players are still ongoing, display dealer hand and play dealer hand
        if any('live' in hand.status for hand in player_hands):
            jh.sleep_and_clear(1)
            cards.display_hands(player_hands, dealer_hand, chip_stack.bets, dealer_show=True)

            # Dealer Must Hit Below 17
            while dealer_hand.val < 17:
                print("Dealer Has {}, Must Hit".format(dealer_hand.val))
                jh.sleep_and_clear(1.5)
                dealer_hand = hit(deck, dealer_hand)
                dealer_hand.adjust_for_aces()
                cards.display_hands(player_hands, dealer_hand, chip_stack.bets, dealer_show=True)

            # Check dealer against all hands
            for hand_ix in range(len(player_hands)):

                # Skip if hand is dead, otherwise check dealer value against player
                if 'live' in player_hands[hand_ix].status:
                    jh.sleep_and_clear(1)

                    if dealer_hand.val > 21:
                        player_hands[hand_ix].status = 'win'
                        cards.display_hands(player_hands, dealer_hand, chip_stack.bets, dealer_show=True)
                        print("Player Hand #{}: Dealer Has Busted, Player Wins Wager".format(hand_ix+1))
                        chip_stack.win_bet(hand_ix)

                    elif dealer_hand.val == player_hands[hand_ix].val:
                        player_hands[hand_ix].status = 'push'
                        cards.display_hands(player_hands, dealer_hand, chip_stack.bets, dealer_show=True)
                        print("Player Hand #{}: Push, no glory for either side".format(hand_ix+1))

                    elif dealer_hand.val < player_hands[hand_ix].val:
                        player_hands[hand_ix].status = 'win'
                        cards.display_hands(player_hands, dealer_hand, chip_stack.bets, dealer_show=True)
                        print("Player Hand #{}: Dealer Has {}, Player Has {}, "
                              "Player Wins Wager!".format(hand_ix+1, dealer_hand.val, player_hands[hand_ix].val))
                        chip_stack.win_bet(hand_ix)

                    else:
                        player_hands[hand_ix].status = 'loss'
                        cards.display_hands(player_hands, dealer_hand, chip_stack.bets, dealer_show=True)
                        print("Player Hand #{}: Dealer Has {}, Player Has {}, "
                              "Player Loses Wager".format(hand_ix+1, dealer_hand.val, player_hands[hand_ix].val))
                        chip_stack.lose_bet(hand_ix)

    # End of game
    jh.sleep_and_clear(1)
    print("Sorry to see you go, but I'll enjoy watching you walkaway")


if __name__ == "__main__":
    run_game()
