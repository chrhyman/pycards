class CardError(Exception):
    pass

class Card:
    RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', 'Z']
    SUITS = ['C', 'D', 'H', 'S', 'B', 'R']
    pretty_SUITS = ['♣', '♦', '❤', '♠']

    NAMES = {
        'A': "Ace",
        'B': "Black",
        'C': "Clubs",
        'D': "Diamonds",
        'H': "Hearts",
        'J': "Jack",
        'K': "King",
        'Q': "Queen",
        'R': "Red",
        'S': "Spades",
        'T': "Ten",
        'Z': "Joker",
        '9': "Nine",
        '8': "Eight",
        '7': "Seven",
        '6': "Six",
        '5': "Five",
        '4': "Four",
        '3': "Three",
        '2': "Two"
    }

    def __init__(self, rank='Z', suit='R'):
        rank, suit = rank.upper(), suit.upper()
        if rank not in Card.RANKS or suit not in Card.SUITS:
            raise CardError(f"INVALID Card(): rank={rank}, suit={suit}")

        self.rank = rank
        self.rank_i = Card.RANKS.index(rank)
        self.rank_name = Card.NAMES[rank]

        self.suit = suit
        self.suit_i = Card.SUITS.index(suit)
        self.suit_name = Card.NAMES[suit]

        self.color = "red" if self.suit in ['D', 'H', 'R'] else "black"

    def __repr__(self):
        return f"{self.rank}.{self.suit}"

    def __str__(self):
        if self.suit in ['R', 'B']:
            return f"{self.suit_name} {self.rank_name}"
        else:
            return f"{self.rank_name} of {self.suit_name}"

    def rank_eq(self, other):
        return self.rank == other.rank

    def suit_eq(self, other):
        return self.suit == other.suit

    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __ne__(self, other):
        return self.rank != other.rank or self.suit != other.suit

    def __lt__(self, other):
        if self.rank_i < other.rank_i or (self.rank_i == other.rank_i and self.suit_i < other.suit_i):
            return True
        else:
            return False

    def __le__(self, other):
        if self.rank_i <= other.rank_i or (self.rank_i == other.rank_i and self.suit_i <= other.suit_i):
            return True
        else:
            return False

    def __gt__(self, other):
        if self.rank_i > other.rank_i or (self.rank_i == other.rank_i and self.suit_i > other.suit_i):
            return True
        else:
            return False

    def __ge__(self, other):
        if self.rank_i >= other.rank_i or (self.rank_i == other.rank_i and self.suit_i >= other.suit_i):
            return True
        else:
            return False

    def next_rank(self):
        if self.rank == 'A':
            i = 0 # '2'
        else:
            i = self.rank_i + 1
        return Card.RANKS[i]

    def prev_rank(self):
        if self.rank == '2':
            i = 12 # 'A'
        else:
            i = self.rank_i - 1
        return Card.RANKS[i]

    def _next(self):
        '''Returns a new Card object that is "next" in this order:
        2 of Clubs, 3 of Clubs, ..., King of Clubs, Ace of Clubs,
        2 of Diamonds, ..., Ace of Hearts, 2 of Hearts, ..., Ace of Hearts,
        2 of Spades, ..., Ace of Spades, Red Joker, Black Joker, [repeats]
                 when using empty constructor Card(), BJ ^ is the default card
        '''
        if self.suit_i <= Card.SUITS.index('S'):
            if self.rank_i < Card.RANKS.index('A'):
                return Card(Card.RANKS[self.rank_i + 1], self.suit)
            elif self.rank == 'A':
                if self.suit_i < Card.SUITS.index('S'):
                    return Card('2', Card.SUITS[self.suit_i + 1])
                elif self.suit == 'S':
                    return Card('Z', 'B')
        elif self.suit == 'B' and self.rank == 'Z':
            return Card('Z', 'R')
        elif self.suit == 'R' and self.rank == 'Z':
            return Card('2', 'C')

        raise CardError(f"No next value for r={self.rank}, s={self.suit}")

    def next_n(self, n): # doesn't include itself; returns a list; Card().next_n(52) is an idiom for a list of the standard 52 cards
        card = self
        card_list = []
        for _ in range(n):
            card = card._next()
            card_list.append(card)
        return card_list

    def url(self, show_back=False):
      if show_back:
          return "https://raw.githubusercontent.com/chrhyman/pycards/main/assets/cards/cardback.png"
      return f"https://raw.githubusercontent.com/chrhyman/pycards/main/assets/cards/{self.rank_name.lower()}_{self.suit_name.lower()}.png"
