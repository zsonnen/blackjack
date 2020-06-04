import random
import collections
import time
import os
import visuals

"""
BLACKJACK GAME:
visuals file imported: numerous pretty ways to display cards
"""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_answer(question):
    while True:
        answer = input(question)
        if answer in ['y', 'n']:
            return answer == 'y'


Card = collections.namedtuple('Card', ['value', 'suit'])


class Deck:

    values = [str(v) for v in range(2, 11)] + list('JQKA')
    suits = "Spades Diamonds Hearts Clubs".split()
    suit_symbols = ['♠','♦','♥','♣']

    def __init__(self):
        # super(Deck, self).__init__()
        self.cards = [Card(value, suit) for suit in self.suits for value in self.values]

    def __repr__(self):
        deck_cards = "Deck()\n"
        for card in self.cards:
            deck_cards += f"({card.value}-{card.suit})"
        return deck_cards

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]

    def __add__(self, other):
        assert isinstance(other, type(self))
        larger_deck = self.__class__()
        larger_deck.cards = self.cards[:] + other.cards[:]
        return larger_deck

    def shuffle(self):
        random.shuffle(self.cards)

    def draw_card(self):
        return self.cards.pop()

    def reset(self):
        self.cards = [Card(value, suit) for suit in self.suits for value in self.values]

    def sort_deck(self):
        suit_ranks = dict(Spades=3, Hearts=2, Diamonds=1, Clubs=0)

        def card_rank(card):
            rank = self.values.index(card.value)
            return rank * len(suit_ranks) + suit_ranks[card.suit]

        self.cards = sorted(self.cards, key=card_rank)

    def deck_visual(self):
        spades, diamonds, hearts, clubs = [], [], [], []

        for card in self.cards:
            card_vis = visuals.tiny_card_visual(card)

            if card.suit == 'Spades':
                spades.append(card_vis)
            elif card.suit == 'Diamonds':
                diamonds.append(card_vis)
            elif card.suit == 'Hearts':
                hearts.append(card_vis)
            else:
                clubs.append(card_vis)

        visuals.print_cards(spades)
        visuals.print_cards(diamonds)
        visuals.print_cards(hearts)
        visuals.print_cards(clubs)

    def deck_card_visuals(self):
        card_list = []
        for card in self.cards:
            card_vis = visuals.tiny_card_visual(card)
            card_list.append(card_vis)

        for card in card_list:
            visuals.print_card(card)


class MultiDeck(Deck):

    def __init__(self, num_decks):
        Deck.__init__(self)
        self.values = Deck.values * num_decks

    # reshuffle when deck is < 50% length
    def is_shuffle_time(self, num_decks):
        return  len(self) < (len(MultiDeck(num_decks))/2)

    def shuffle_time(self):
        print("Reshuffling the Deck...\n")
        time.sleep(1)
        print("Reshuffling the Deck...\n")
        time.sleep(1)
        print("Reshuffling the Deck...\n")
        time.sleep(1)
        self.reset()
        self.shuffle()


class Hand:

    def __init__(self):
        # super(Hand, self).__init__()
        self.hand = []

    def __repr__(self):
        hand_cards = "Hand()\n"
        for card in self.hand:
            hand_cards += f"({card.value}-{card.suit})"
        return hand_cards

    def add(self, *cards):
        for card in cards:
            self.hand.append(card)

    def remove_card(self):
        return self.hand.pop()

    def hit(self, deck):
        assert isinstance(deck, type(Deck()))
        card = deck.draw_card()
        self.add(card)

    def hand_score(self):
        score = 0
        for card in self.hand:
            if card.value in ['J','Q','K']:
                card_score = 10
            elif card.value == 'A':
                card_score = 1
            else:
                card_score = int(card.value)
            score += card_score
        if any(card.value == 'A' for card in self.hand) and score <= 11:
            score += 10

        return score

    def card_visual(self):
        card_list = []
        for card in self.hand:
            card_vis = visuals.reg_card_visual(card)
            card_list.append(card_vis)

        visuals.print_cards(card_list)
        print(f"\nTotal of: {self.hand_score()}\n")

    def mini_card_visual(self):
        card_list = []
        for card in self.hand:
            card_vis = visuals.mini_card_visual(card)
            card_list.append(card_vis)

        visuals.print_cards(card_list)
        print(f"\nTotal of: {self.hand_score()}\n")


class Player(Hand):

    def __init__(self, chips):
        Hand.__init__(self)
        # super(Player, self).__init__()
        self.chips = chips
        self.bet = 0
        self.alive = True
        self.split_cards = False

    def add_chips(self, chips):
        self.chips += chips

    def remove_chips(self, chips):
        self.chips -= chips

    def reset(self):
        self.hand = []
        self.alive = True
        self.split_cards = False
        self.bet, self.bet_two = 0, 0

    def has_black_jack(self):
        return len(self.hand) == 2 and self.hand_score() == 21

    def wager(self):
        while True:
            bet = input(f"You have ${self.chips:,.2f} \nHow much would you like to bet?: $")
            if not bet.isdecimal():
                print("invalid entry. try again")
                continue
            if float(bet) > self.chips:
                print("sorry, you dont have enough chips. Try again")
            else:
                self.bet = float(bet)
                self.remove_chips(float(bet))
                break

    def added_wager(self):
        while True:
            other_bet = input(f"\nEnter additional wager. You may bet up to your original ${self.bet} or less: $")
            if not other_bet.isdecimal() or float(other_bet) > self.bet:
                print("invalid entry. try again")
                continue
            elif float(other_bet) > self.chips:
                print("You dont have enough chips. Try again")
            else:
                self.bet_two = float(other_bet)
                self.remove_chips(float(other_bet))
                break

    def double_down(self):
        if len(self.hand) == 2:
            if validate_answer("\nYou will only get 1 more card. Confirm you want to double down: [y / n]: "):
                self.added_wager()
                self.bet += self.bet_two

    def check_for_split(self):
        if self.hand[0].value == self.hand[1].value:
            if validate_answer("Do you want to split your cards?: [y / n]: "):
                self.split_cards = True


    def apply_split(self, deck):
        if self.split_cards:
            self.added_wager()
            self.hand_two = Player(0)
            self.hand_two.split_cards = True
            self.hand_two.bet = self.bet_two

            transfer_card = self.remove_card()
            self.hand_two.add(transfer_card)
            self.hit(deck)
            self.hand_two.hit(deck)

            print("\nFirst Hand: ")
            self.mini_card_visual()
            time.sleep(1)
            self.player_move(deck)

            print("\nSecond Hand: ")
            self.hand_two.mini_card_visual()
            time.sleep(1)
            self.hand_two.player_move(deck)


    def remaining_chips(self):
        time.sleep(1)
        print(f"You have ${self.chips} remaining\n")

    def player_move(self, deck):
        assert isinstance(deck, type(Deck()))
        while True:
            if self.hand_score() > 21:
                self.alive = False
                break
            if self.hand_score() == 21:
                break
            if len(self.hand) == 2:
                action = input("Would you like to hit, stand, or double-down: Enter [h, s, or d]: ")
                if action == "d":
                    self.double_down()
                    self.hit(deck)
                    self.card_visual()
                    if self.hand_score() > 21:
                        self.alive = False
                    break
            else:
                action = input("Would you like to hit or stand: Enter [h or s]: ")
                if action not in ['h', 's']:
                    print('invalid input. try again')
            if action == "h":
                self.hit(deck)
                if self.split_cards:
                    self.mini_card_visual()
                else:
                    self.card_visual()
            if action == "s":
                break

    def compute_results(self, dealer):
        assert isinstance(dealer, type(Dealer()))
        if self.alive and dealer.alive:
            if self.hand_score() > dealer.hand_score():
                print("WINNER!!\n")
                self.add_chips(self.bet * 2)

            elif self.hand_score() == dealer.hand_score():
                print("PUSH!!\n")
                self.add_chips(self.bet)
            else:
                print("LOSER!! Dealer Wins\n")

        elif not self.alive:
            print("BUST!! LOSER!!\n")

        else:
            print("DEALER BUSTS. YOU WIN!!\n")
            self.add_chips(self.bet * 2)


class Dealer(Hand):

    def __init__(self):
        Hand.__init__(self)
        # super(Dealer, self).__init__()
        self.alive = True

    def reset(self):
        self.hand = []
        self.alive = True

    def card_reveal(self):
        time.sleep(1)
        print("\n________________{Dealer Cards}__________________________\n")
        time.sleep(1)
        self.card_visual()
        time.sleep(1)

    def dealer_move(self, deck):
        self.card_reveal()
        while True:
            if self.hand_score() in range(17, 22):
                return True
            if self.hand_score() > 21:
                self.alive = False
                return False

            if self.hand_score() < 17:
                self.hit(deck)
                time.sleep(1)
                self.card_visual()

    def dealer_visual(self):
        card_list = []

        hidden_card = visuals.reg_hidden_card
        card_list.append(hidden_card)

        for card in self.hand[1:]:
            card_vis = visuals.reg_card_visual(card)
            card_list.append(card_vis)

        visuals.print_cards(card_list)


def play_again():
    if validate_answer("Would you like to play another round? [y / n]: "):
        clear()
        return True
    return False


def game():
    print("\n______________________WELCOME TO BLACKJACK!!_______________________\n")

    num_decks    = 1
    player_chips = 1_000

    player =  Player(player_chips)
    dealer =  Dealer()
    deck   =  MultiDeck(num_decks)

    deck.shuffle()

    while True:
        if deck.is_shuffle_time(num_decks):
            deck.shuffle_time()

        player.hit(deck)
        dealer.hit(deck)
        player.hit(deck)
        dealer.hit(deck)
        player.wager()

        print("\n________________{Dealer Cards}__________________________\n")
        dealer.dealer_visual()
        time.sleep(1)
        print("\n________________[Player Cards]__________________________\n")
        player.card_visual()

        if player.has_black_jack():
            print("YOU HAVE BLACKJACK!\n")
            player.add_chips(player.bet * 2.5)
            player.remaining_chips()
            player_chips = player.chips
            if play_again():
                player.reset()
                dealer.reset()
                continue
            else:
                break

        player.check_for_split()
        player.apply_split(deck)
        time.sleep(1)

        if not player.split_cards:
            player.player_move(deck)
            if player.alive:
                dealer.dealer_move(deck)
            player.compute_results(dealer)

            player_chips = player.chips
            player.remaining_chips()
            if play_again():
                player.reset()
                dealer.reset()
                continue
            else:
                break

        # PLAYER SPLIT CARDS
        else:
            if player.alive or player.hand_two.alive:
                dealer.dealer_move(deck)

            print("HAND ONE:")
            player.compute_results(dealer)
            print("HAND TWO:")
            player.hand_two.compute_results(dealer)

            # Any chips won by second hand: Add it to total balance
            player.chips += player.hand_two.chips
            player_chips = player.chips
            player.remaining_chips()
            if play_again():
                player.reset()
                dealer.reset()
                continue
            else:
                break

    print("Thanks for playing. Goodbye.")

if __name__ == "__main__":
    game()
