# BlackJack cardgame
 
`visuals` file contains variety of ways to represent cards. a nicer, prettier way to output to user  
 - note: if terminal width is too narrow, it may have an affect on the way cards are outputed

Game is played with 6 52-card Decks

Standard casino rules:  
  - Player vs Dealer: 
  - Player starts with $1,000.00 to wager with. Ability to continue playing until balance hits $00.00
  - Both dealt two cards, with Dealer having one face down or hidden. 
  - Player goes first, and chooses if they want to hit or stay. 
  - Option to `Double Down`:
    - player may enter additional wager up to, but not greater than original wager. 
    - If chosen, player receives one more card, and only one more card. 
  - Option to `Split`:
    - If chosen, player may place down an additional wager, for the second hand.   
    - The second wager can be up to, but no greater than original wager
    
  - Player is able to double down after splitting as well
    
  - If upon hit, the player's hand sums to over 21, player loses  
  - Dealer must continue hitting, until sum of hand is at least 17. If over 21, dealer busts, and player wins  
    
  - If initial two cards dealt add to 21, player has `BlackJack` and is paid at 1.5:1 wager placed (ex: getting a BlackJack on an $100 wager would earn $150)   
    
  - Any non-blackjack win: hand is paid 1:1 match of wager placed for that hand
