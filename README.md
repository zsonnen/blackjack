# BlackJack

## BlackJack cardgame  
visuals file contains variety of ways to represent cards. a nicer, prettier way to output to user. 
If terminal width is too narrow, it may have an affect on the way cards are outputed

Player vs Dealer
Player gets $1,000.00 to wager with, that updates after each round. Ability to continue playing until balance hits $00.00

Game is played with 4 52-Card Decks. 

Standard casino rules:
  Player vs Dealer: 
  Both dealt two cards, with Dealer having one face down or hidden. Player goes first, and chooses if they want to hit or stay  
  If upon hit, the player's hand sums to over 21, player loses
  Dealer must continue hitting, until sum of hand is at least 17. If over 21, dealer busts, and player wins
  
  If initial two cards dealt add to 21, player has `BlackJack` and receives 1.5x bet placed
  If initial two cards have the same value, player has the option to 'Split'
    If the player chooses to split their cards, they must place down an additional bet. 
    The bet can match the value of original bet, or be any amount up to but not larger than original
    
  If player wins the round, they receive 1:1 match of bet placed for that hand
