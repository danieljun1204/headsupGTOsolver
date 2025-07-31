import random

CARDS = ['J', 'Q', 'K']

def deal():
    deck = CARDS[:]
    random.shuffle(deck)
    return deck[:2]

def is_terminal(history):
    terminal_histories = {
        'check-check',
        'check-bet-call',
        'check-bet-fold',
        'bet-call',
        'bet-fold',
    }
    return history in terminal_histories

def payoff(history, cards):
    p0, p1 = cards
    if history.endswith('fold'):
        # If fold happens, the player who did NOT fold wins.
        # Even # of actions ⇒ P1 folded ⇒ P0 wins; odd ⇒ P0 folded ⇒ P1 wins
        return 1 if len(history.split('-')) % 2 == 0 else -1
    # showdown: higher card wins
    winner = 0 if CARDS.index(p0) > CARDS.index(p1) else 1
    return 1 if winner == 0 else -1

def get_legal_actions(history):
    """
    Returns the list of legal actions at each decision point.
    """
    if history == '':
        return ['check', 'bet']
    elif history == 'check':
        return ['check', 'bet']
    elif history == 'bet':
        return ['call', 'fold']
    elif history == 'check-bet':
        return ['call', 'fold']
    else:
        return []  # terminal state
