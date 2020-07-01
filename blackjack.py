from __future__ import annotations
import random
import collections
import time
import os
from typing import Sequence
import subprocess as sp 
import visuals


"""
BLACKJACK GAME:
visuals file imported: numerous pretty ways to display cards
"""

def clear():
    sp.run(('cls' if os.name == 'nt' else 'clear'), shell=True)

def validate_answer(question: str, choices: Sequence[str]) -> bool:
    while answer := input(question).lower():
        if answer in choices:
            return answer == choices[0]

YES_NO = 'yn'


Card = collections.namedtuple('Card', ['value', 'suit'])

class Deck:

    values = [str(v) for v in range(2, 11)] + list('JQKA')
    suits = "Spades Diamonds Hearts Clubs".split()
    suit_symbols = ['♠','♦','♥','♣']

    def __init__(self, num_decks=1):
        self.num_decks = num_decks
        self.cards = [Card(value, suit) for suit in self.suits for value in self.values] * self.num_decks
        self.length = len(self)

    def __repr__(self):
        return "Deck()\n" + ''.join(f"({card.value}-{card.suit})" for card in self.cards)

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]
    
    def __setitem__(self, position, value):
        self.cards[position] = value

    def draw_card(self):
        return self.cards.pop()    

    def shuffle(self):
        random.shuffle(self.cards)
    
    #Shuffle when deck is < 50% full length
    def is_shuffle_time(self):
        return  len(self) < (self.length / 2)
    
    def shuffle_time(self):
        clear()
        print("Reshuffling the Deck...\n")
        time.sleep(1)
        self.reset()
        self.shuffle()    

    def reset(self):
        self.cards = [Card(value, suit) for suit in self.suits for value in self.values] * self.num_decks

    def deck_visual(self):
        s = [visuals.tiny_card_visual(card) for card in self.cards if card.suit == 'Spades']
        d = [visuals.tiny_card_visual(card) for card in self.cards if card.suit == 'Diamonds']
        h = [visuals.tiny_card_visual(card) for card in self.cards if card.suit == 'Hearts']
        c = [visuals.tiny_card_visual(card) for card in self.cards if card.suit == 'Clubs']
        visuals.print_cards(s)
        visuals.print_cards(d)
        visuals.print_cards(h)
        visuals.print_cards(c)

class Hand:

    def __init__(self):
        self.hand = []

    def __repr__(self):
        return "Hand()\n" + ''.join(f"({card.value}-{card.suit})" for card in self.hand)

    def add_card(self, *cards: Card) -> None:
        for card in cards:
            self.hand.append(card)

    def remove_card(self):
        return self.hand.pop()

    def hit(self, deck: Deck) -> None:
        card = deck.draw_card()
        self.add_card(card)
    
    def hand_score(self) -> int:
        self.card_val = [10 if card.value in ['J','Q','K'] else 1 if card.value == 'A'
                         else int(card.value) for card in self.hand]

        self.card_scores = dict(zip(self.hand, self.card_val))
        score = 0
        for card in self.hand:
            card_score = self.card_scores[card]
            score += card_score
        if any(card.value == 'A' for card in self.hand) and score <= 11:
            score += 10
        return score
    
    def card_visual(self):
        card_list = [visuals.reg_card_visual(card) for card in self.hand]
        visuals.print_cards(card_list)
        print(f"\nTotal of: {self.hand_score()}\n")

    def mini_card_visual(self):
        card_list = [visuals.mini_card_visual(card) for card in self.hand]
        visuals.print_cards(card_list)
        print(f"\nTotal of: {self.hand_score()}\n")

class Player(Hand):

    def __init__(self, chips, bet=0, split_cards=False):
        super().__init__()
        self.chips = chips
        self.bet = bet
        self.profit = 0
        self.alive = True
        self.split_cards = split_cards
        self.has_blackjack = False
    
    def deal_cards(self, deck: Deck) -> None:
        self.hit(deck)
        self.hit(deck)
        print_line('Player Cards')
        self.card_visual()  
        self.has_blackjack = self.check_for_blackjack()
        self.split_cards = self.check_for_split()
        self.apply_split(deck)

    def add_chips(self, chips: float) -> None:
        self.chips += chips

    def remove_chips(self, chips: float) -> None:
        self.chips -= chips

    def print_balance(self): 
        print(f"\nYour balance is currently: ${self.chips:,.2f}\n")

    def check_for_blackjack(self):
        return len(self.hand) == 2 and self.hand_score() == 21
    
    def check_for_split(self):
        if self.hand[0].value == self.hand[1].value:
            return validate_answer("Do you want to split your cards?: [y / n]: ", YES_NO)            
        return False

    def wager(self):
        while True:
            self.print_balance()
            bet = input(f"How much would you like to bet?: $")
            if not bet.isdecimal():
                continue
            elif float(bet) > self.chips:
                print("sorry, you don't have enough chips. Try again")
            else:
                self.bet = float(bet)
                self.remove_chips(float(bet))
                break

    def added_wager(self):
        while True:
            self.print_balance()
            bet = input(f"Enter additional wager. You may bet up to your original ${self.bet} or less: $")
            if not bet.isdecimal() or float(bet) > self.bet:
                continue
            elif float(bet) > self.chips:
                print("You don't have enough chips. Try again")
            else:
                self.bet_two = float(bet)
                self.remove_chips(float(bet))
                break

    def confirm_double(self):
        return validate_answer("\nYou will only get 1 more card. Confirm you want to double down: [y / n]: ", YES_NO)

    def double_down(self, deck: Deck) -> None:
        self.added_wager()
        self.bet += self.bet_two
        self.visual_move(deck)
        if self.hand_score() > 21:
            self.alive = False

    def apply_split(self, deck: Deck) -> None:
        if self.split_cards:
            self.added_wager()
            self.hand_two = Player(0, split_cards=True, bet=self.bet_two)

            transfer_card = self.remove_card()
            self.hand_two.add_card(transfer_card)
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
            time.sleep(1)

    def visual_move(self, deck: Deck) -> None:
        self.hit(deck)
        if self.split_cards:
            self.mini_card_visual()
        else:
            self.card_visual()

    def player_move(self, deck: Deck) -> None:
        while True:
            if self.hand_score() > 21 or self.has_blackjack:
                self.alive = False
                break
            if self.hand_score() == 21:
                break
            if len(self.hand) == 2:
                action = input("Would you like to hit, stand, or double-down? Enter [h, s, or d]: ")
            else:
                action = input("Would you like to hit or stand: Enter [h or s]: ")
            if action == 'd':
                if len(self.hand) == 2:
                    if self.confirm_double():
                        self.double_down(deck)
                        break
            if action == "h":
                self.visual_move(deck)
            if action == "s":
                break

    def compute_results(self, dealer: Dealer) -> None:
        if self.alive and dealer.alive:
            if self.hand_score() > dealer.hand_score():
                print("WINNER!\n")
                self.profit = 2
            elif self.hand_score() == dealer.hand_score():
                print("PUSH!\n")
                self.profit = 1
            else:
                print("LOSER! Dealer Wins\n")

        elif not self.alive:
            if self.has_blackjack:
                print("YOU HAVE BLACKJACK!\n")
                self.profit = 2.5
            else:
                print("BUST! LOSER!\n")
        else:
            print("DEALER BUSTS. YOU WIN!\n")
            self.profit = 2
        self.settle()

    def settle(self):
        self.add_chips(self.profit*self.bet)

    def reset(self):
        self.hand = []
        self.alive = True
        self.split_cards = False
        self.profit = 0
        self.bet, self.bet_two = 0, 0

class Dealer(Hand):

    def __init__(self):
        super().__init__()
        self.alive = True
    
    def deal_cards(self, deck: Deck) -> None:
        self.hit(deck)
        self.hit(deck)
        print_line('Dealer Cards')
        self.dealer_visual()
        time.sleep(1)

    def reset(self):
        self.hand = []
        self.alive = True

    def card_reveal(self):
        print_line('Dealer Cards')
        time.sleep(0.5)
        self.card_visual()
        time.sleep(0.5)

    def dealer_move(self, deck: Deck) -> None:
        self.card_reveal()
        while True:
            if self.hand_score() in range(17, 22):
                break
            if self.hand_score() > 21:
                self.alive = False
                break
            if self.hand_score() < 17:
                self.hit(deck)
                time.sleep(1)
                self.card_visual()

    def dealer_visual(self):
        hidden_card = visuals.reg_hidden_card
        card_list = [hidden_card] + [visuals.reg_card_visual(card) for card in self.hand[1:]]
        visuals.print_cards(card_list)

def play_again() -> bool:
    if validate_answer("Would you like to play another round? [y / n]: ", YES_NO):
        clear()
        return True
    return False

def print_line(word: str) -> None:
    print(f"\n______________________[{word}]______________________________\n")
    

def game():
    print_line('WELCOME TO BLACKJACK!!')
    num_decks = 6
    player_chips = 1_000

    player = Player(player_chips)
    dealer = Dealer()
    deck = Deck(num_decks)

    deck.shuffle()

    while True:
        if player.chips == 0:
            print("You're out of money. Game Over")
            break
        print(f"Percentage of shoe not yet dealt: {len(deck)/(52*num_decks):.2%}")
        if deck.is_shuffle_time():
            deck.shuffle_time()        

        player.wager()
        dealer.deal_cards(deck)
        player.deal_cards(deck)        

        if not player.split_cards:
            player.player_move(deck)
            if player.alive:
                dealer.dealer_move(deck)
            player.compute_results(dealer)        
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

        player.print_balance()
        if play_again():
            player.reset()
            dealer.reset()
            continue
        else:
            break

    print("Thanks for playing. Goodbye.")

if __name__ == "__main__":
    game()
