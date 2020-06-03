"""

Variety of ways to nicely dislay card representations

Width of terminal may impact visual

"""


def print_cards(cardlist):
    for card in zip(*cardlist):
            print('   '.join(card))

def print_card(*cards):
    for line in zip(*cards):
        print('   '.join(line))


def reg_card_visual(card):
    suits = "Spades Diamonds Hearts Clubs".split()
    suit_symbols = ['♠','♦','♥','♣']
    suit_pairs = dict(zip(suits, suit_symbols))

    v = card.value
    s = suit_pairs[card.suit]

    visual = [

         '  ╔════════════╗',
        f'  ║ {v:<5}      ║',
         '  ║            ║',
         '  ║            ║',
        f'  ║     {s:^3}    ║',
         '  ║            ║',
         '  ║            ║',
         '  ║            ║',
        f'  ║      {v:>5} ║',
         '  ╚════════════╝'
    ]

    return visual


def mini_card_visual(card):
    suits = "Spades Diamonds Hearts Clubs".split()
    suit_symbols = ['♠','♦','♥','♣']
    suit_pairs = dict(zip(suits, suit_symbols))

    v = card.value
    s = suit_pairs[card.suit]

    visual = [
         '╔══════╗',
        f'║ {v:<3}  ║',
        f'║      ║',
        f'║  {s:>3} ║',
         '╚══════╝'
         ]

    return visual


def tiny_card_visual(card):
    suits = "Spades Diamonds Hearts Clubs".split()
    suit_symbols = ['♠','♦','♥','♣']
    suit_pairs = dict(zip(suits, suit_symbols))

    v = card.value
    s = suit_pairs[card.suit]

    visual = [
         '╔════╗',
        f'║ {v:<2} ║',
        f'║ {s:>2} ║',
         '╚════╝'     ]

    return visual


def large_card_visual(card):
    suits = "Spades Diamonds Hearts Clubs".split()
    suit_symbols = ['♠','♦','♥','♣']
    suit_pairs = dict(zip(suits, suit_symbols))

    v = card.value
    s = suit_pairs[card.suit]

    visual = [

         '   ┌─────────────────┐',
        f'   │ {v:<5}           │',
         '   │                 │',
         '   │                 │',
         '   │                 │',
         '   │                 │',
        f'   │        {s}        │',
         '   │                 │',
         '   │                 │',
         '   │                 │',
         '   │                 │',
         '   │                 │',
        f'   │           {v:>5} │',
         '   └─────────────────┘'

    ]

    return visual


reg_hidden_card = [
     '   ╔════════════╗',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ╚════════════╝'
     ]


v, s = 'V', 'S'

card_visuals = {

'small_card_vis' : [
     '╔══════╗',
    f'║ {v:<3}  ║',
    f'║ {s:>3}  ║',
    f'║      ║',
     '╚══════╝'
     ],


'mini_card_vis' : [
     '╔══════╗',
    f'║ {v:<3}  ║',
    f'║      ║',
    f'║  {s:>3} ║',
     '╚══════╝'
     ],


'thick_border_vis' : [

     '  ╔════════════╗',
    f'  ║ {v:<5}      ║',
     '  ║            ║',
     '  ║            ║',
    f'  ║     {s:^3}    ║',
     '  ║            ║',
     '  ║            ║',
     '  ║            ║',
    f'  ║      {v:>5} ║',
     '  ╚════════════╝'
     ],


'thin_border_vis' : [

    f'   ┌───────────┐',
    f'   │ {v:<5}     │',
     '   │           │',
     '   │           │',
     '   │           │',
    f'   │     {s}     │',
     '   │           │',
     '   │           │',
     '   │           │',
    f'   │     {v:>5} │',
     '   └───────────┘'
     ]

}

# print_card(card_visuals['thick_border_vis'])


hidden_cards = {


'mini_thick_hidden_card' : [
     '╔══════╗',
     '║░░░░░░║',
     '║░░░░░░║',
     '║░░░░░░║',
     '╚══════╝'
     ],


'reg_thick_hidden_card' : [
     '   ╔════════════╗',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ║░░░░░░░░░░░░║',
     '   ╚════════════╝'
     ],


'small_thin_hidden_card' : [

     '┌────────┐',
     '│░░░░░░░░│',
     '│░░░░░░░░│',
     '│░░░░░░░░│',
     '│░░░░░░░░│',
     '│░░░░░░░░│',
     '└────────┘'
     ],

'reg_thin_hidden_card' : [
     '   ┌───────────┐',
     '   │░░░░░░░░░░░│',
     '   │░░░░░░░░░░░│',
     '   │░░░░░░░░░░░│',
     '   │░░░░░░░░░░░│',
     '   │░░░░░░░░░░░│',
     '   │░░░░░░░░░░░│',
     '   │░░░░░░░░░░░│',
     '   │░░░░░░░░░░░│',
     '   │░░░░░░░░░░░│',
     '   └───────────┘'
     ],

'large_thin_hidden_card' : [
 '   ┌─────────────────┐',
 '   │░░░░░░░░░░░░░░░░░│',
 '   │░░░░░░░░░░░░░░░░░│',
 '   │░░░░░░░░░░░░░░░░░│',
 '   │░░░░░░░░░░░░░░░░░│',
 '   │░░░░░░░░░░░░░░░░░│',
 '   │░░░░░░░░░░░░░░░░░│',
 '   │░░░░░░░░░░░░░░░░░│',
 '   │░░░░░░░░░░░░░░░░░│',
 '   │░░░░░░░░░░░░░░░░░│',
 '   │░░░░░░░░░░░░░░░░░│',
 '   │░░░░░░░░░░░░░░░░░│',
 '   │░░░░░░░░░░░░░░░░░│',
 '   └─────────────────┘'
]

}

# print_card(hidden_cards['reg_thick_hidden_card'])
