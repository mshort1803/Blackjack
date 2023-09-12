import random, sys

# Set up the constants
HEARTS = chr(9829)
DIAMONDS = chr(9830)
SPADES = chr(9824)
CLUBS = chr(9827)

BACKSIDE = 'backside'

def main():
    print('''Blackjack by Michael Short

    Rules:
        Try to get as close to 21 without going over.
        Kings, Queens, and Jacks are worth 10 points.
        Aces are worth 1 or 11 points.
        Cards 2 through 10 are worth their face value
        (H)it to take another card
        (S)tand to stop taking cards
        On your first play, you can (D)ouble down to increase your bet
        but must hit exactly one more time before standing.
        In case of a tie, the bet is returned to the player
        The dealer stops hitting at 17''')

    money = 5000
    while True: # main game loop
        # Check if the player has run out of money
        if money <= 0:
            print('You\'re broke\nGood thing you are\'nt playing for real money')
            print('Thanks for playing')
            sys.exit()

        # let the player enter their bet for this round
        print('Money:', money)
        bet = getBet(money)

        # Give the dealer and player 2 cards from the deck each
        deck = getDeck()
        dealerHand = [deck.pop(), deck.pop()]
        playerHand = [deck.pop(), deck.pop()]

        # Handle player actions
        print('Bet: ', bet)
        while True: # keep looping until player stands or busts
            displayHands(playerHand, dealerHand, False)
            print()

            # Check if the player has bust
            if getHandValue(playerHand) > 21:
                break

            # Get the player's move, either H, S or D
            move = getMove(playerHand, money - bet)

            # Handle the player actions
            if move == 'D':
                # Player is doubling down, they can increase their bet
                additionalBet = getBet(min(bet, (money - bet)))
                bet += additionalBet
                print('Bet increased to {}.'.format(bet))
                print('Bet:', bet)

            if move in ('H', 'D'):
                # Hit/doubling down takes another card.
                newCard = deck.pop()
                rank, suit = newCard
                print('You drew a {} of {}.'.format(rank, suit))
                playerHand.append(newCard)

                if getHandValue(playerHand) > 21:
                    # the player has busted
                    continue

            if move in ('S', 'D'):
                # Stand, doubling down stops the players turn.
                break

        # Handle the dealer's actions.
        if getHandValue(playerHand) <= 21:
            while getHandValue(dealerHand) < 17:
                # The dealer hits
                print('Dealer hits...')
                dealerHand.append(deck.pop())
                displayHands(playerHand, dealerHand, False)

                if getHandValue(dealerHand) > 21:
                    break # Dealer has buste

                input('Press Enter to continue')
                print('\n\n')


        displayHands(playerHand, dealerHand, True)

        playerValue = getHandValue(playerHand)
        dealerValue = getHandValue(dealerHand)
        # Handle whether the player has won, lost, or tied
        if dealerValue > 21:
            print('The dealer busts, you win ${}!'.format(bet))
            money += bet
        elif (playerValue > 21) or (playerValue < dealerValue):
            print('You lost!')
            money -= bet
        elif playerValue > dealerValue:
            print('You won ${}!'.format(bet))
            money += bet
        elif playerValue == dealerValue:
            print('it\'s a tie, the bet was returned to you.')

        input('Press enter to continue')
        print('\n\n')


def getBet(maxBet):
    """Ask the player how much they would like to bet for this round"""
    while True:
        print('How do you bet? (1-{}, or QUIT)'.format(maxBet))
        bet = input('> ').upper().strip()
        if bet == 'QUIT':
            print('thanks for playing')
            sys.exit()

        if not bet.isdecimal():
            continue

        bet = int(bet)
        if 1 <= bet <= maxBet:
            return bet

def getDeck():
     """Return a list of (rank, suit) tuples for all 52 cards."""
     deck = []
     for suit in (HEARTS, DIAMONDS, SPADES, CLUBS):
         for rank in range(2, 11):
             deck.append((str(rank), suit))
         for rank in  ('J', 'Q', 'K', 'A'):
             deck.append((rank, suit))
     random.shuffle(deck)
     return deck

def displayHands(playerHand, dealerHand, showDealerHand):
    """Show the player's and the dealer's cards. Hide the dealer's cards first
    card if showDealerHand is False"""
    print()
    if showDealerHand:
        print('DEALER:', getHandValue(dealerHand))
        displayCards(dealerHand)
    else:
        print('DEALER: ???')
        # Hide the dealer's first card:
        displayCards([BACKSIDE] + dealerHand[1:])

    # Show the player's cards
    print('PLAYER:', getHandValue(playerHand))
    displayCards(playerHand)

def getHandValue(cards):
    """Returns the value of the cards. Face cards are worth 10 , aces are worth 11 or 1
    this function picks the most suitable ace value)."""
    value = 0
    numberOfAces = 0

    # Add the value for the non-ace cards
    for card in cards:
        rank = card[0]
        if rank == 'A':
            numberOfAces += 1
        elif rank in ('K', 'Q', 'J'):
            value += 10
        else:
            value += int(rank)

    # Add the value for the aces
    value += numberOfAces # add 1 per ace
    for i in range(numberOfAces):
        # If another 11 can be added without busting, do so
        if value + 10 <= 21:
            value += 10

    return value

def  displayCards(cards):
    """Display all the cards in the cards list"""
    rows = ['', '', '', '', '']

    for i, card in enumerate(cards):
        rows[0] += '  __ '  #Print the top of the card.
        if card == BACKSIDE:
            # print a card's back
            rows[1] += '|## | '
            rows[2] += '|###| '
            rows[3] += '|_##| '
        else:
            # Print the card's front:
            rank, suit = card
            rows[1] += '|{} | '.format(rank.ljust(2))
            rows[2] += '| {} | '.format(suit)
            rows[3] += '|_{}| '.format(rank.rjust(2, '_'))

        # print each row on the screen
        for row in rows:
            print(row)

def getMove(playerHand, money):
    """Asks the player for their move, and returns 'H' for hit 'S' for
    stand, and 'D' for double down"""
    while True:
        # Determine what moves the player can make:
        moves = ['(H)it', '(S)tand']

        # The player can double down on their first move, which we can
        # tell because they'll have exactly 2 cards
        if len(playerHand) ==  2 and money > 0:
            moves.append('(D)ouble Down')

        # Get the player's move
        movePrompt = ', '.join(moves) + '> '
        move = input(movePrompt).upper()
        if move in ('H',  'S'):
            return move
        if move == 'D' and '(D)ouble Down' in moves:
            return move

if __name__ == '__main__':
    main()
    
            
