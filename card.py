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

class CardError(Exception):
    pass

class RankError(CardError):
    pass

class SuitError(CardError):
    pass

class Rank:
    RANKS = ['2', '3', '4', '5', '6', '7', '8',
             '9', 'T', 'J', 'Q', 'K', 'A', 'Z']
    def __init__(self, rank='Z'):
        rank = rank.upper()
        if rank not in Rank.RANKS:
            raise RankError(f"INVALID Rank: rank={rank}")
        self.rank = rank
        self.rank_i = Rank.RANKS.index(rank)
        self.rank_name = NAMES[rank]

    def __repr__(self):
        return f"Rank('{self.rank}')"

    def __str__(self):
        return self.rank

    def __eq__(self, other):
        if type(other) is not type(self):
            if type(other) is Card:
                return self.__eq__(other.rk)
            else:
                return False
        else:
            return self.rank == other.rank

    def __ne__(self, other):
        if type(other) is not type(self):
            if type(other) is Card:
                return self.__ne__(other.rk)
            else:
                return True
        else:
            return self.rank != other.rank

    def __lt__(self, other):
        return self.rank_i < other.rank_i

    def __le__(self, other):
        return self.rank_i <= other.rank_i

    def __gt__(self, other):
        return self.rank_i > other.rank_i

    def __ge__(self, other):
        return self.rank_i >= other.rank_i

    def _next(self):
        if self.rank in ['A', 'Z']:
            i = 0 # '2'
        else:
            i = self.rank_i + 1
        return Rank(Rank.RANKS[i])

    def run_of(self, n): # returns list of n sequential Ranks starting w/ self
        rank = self
        rank_list = []
        for _ in range(n):
            rank_list.append(rank)
            rank = rank._next()
        if Rank('A') in rank_list[1:-1]:
            raise RankError("An Ace is in the middle of a run.")
        return rank_list

class Suit:
    SUITS = ['C', 'D', 'H', 'S', 'B', 'R']
    def __init__(self, suit='R'):
        suit = suit.upper()
        if suit not in Suit.SUITS:
            raise SuitError(f"INVALID Suit: suit={suit}")
        self.suit = suit
        self.suit_i = Suit.SUITS.index(suit)
        self.suit_name = NAMES[suit]
        self.color = "red" if self.suit in ['D', 'H', 'R'] else "black"

    def __repr__(self):
        return f"Suit('{self.suit}')"

    def __str__(self):
        return self.suit

    def __eq__(self, other):
        if type(other) is not type(self):
            if type(other) is Card:
                return self.__eq__(other.st)
            else:
                return False
        else:
            return self.suit == other.suit

    def __ne__(self, other):
        if type(other) is not type(self):
            if type(other) is Card:
                return self.__ne__(other.st)
            else:
                return True
        else:
            return self.suit != other.suit

    def __lt__(self, other):
        return self.suit_i < other.suit_i

    def __le__(self, other):
        return self.suit_i <= other.suit_i

    def __gt__(self, other):
        return self.suit_i > other.suit_i

    def __ge__(self, other):
        return self.suit_i >= other.suit_i

    def _next(self):
        if self.suit in ['S', 'B', 'R']:
            i = 0 # 'C'
        else:
            i = self.suit_i + 1
        return Suit(Suit.SUITS[i])

class Card:
    def __init__(self, rank='Z', suit='R'): # Card(str(rank_obj), str(suit_obj))
        rank, suit = rank.upper(), suit.upper()
        try:
            self.rk = Rank(rank)
            self.st = Suit(suit)
            self.color = self.st.color
        except:
            raise CardError(f"INVALID Card(): rank={rank}, suit={suit}")

    def __repr__(self):
        return f"{self.rk}.{self.st}"

    def __str__(self):
        if self.st in [Suit('R'), Suit('B')]:
            return f"{self.st.suit_name} {self.rk.rank_name}"
        else:
            return f"{self.rk.rank_name} of {self.st.suit_name}"

    def rank_eq(self, other):
        return self.rk == other.rk

    def suit_eq(self, other):
        return self.st == other.st

    def __eq__(self, other):
        if type(other) is not type(self):
            if type(other) is Rank:
                return other.__eq__(self.rk)
            elif type(other) is Suit:
                return other.__eq__(self.st)
            else:
                return False
        else:
            return self.rk == other.rk and self.st == other.st

    def __ne__(self, other):
        if type(other) is not type(self):
            if type(other) is Rank:
                return other.__ne__(self.rk)
            elif type(other) is Suit:
                return other.__ne__(self.st)
            else:
                return True
        else:
            return self.rk != other.rk or self.st != other.st

    def __lt__(self, other):
        if self.rk < other.rk or (self.rk == other.rk and self.st < other.st):
            return True
        else:
            return False

    def __le__(self, other):
        if self.rk <= other.rk or (self.rk == other.rk and self.st <= other.st):
            return True
        else:
            return False

    def __gt__(self, other):
        if self.rk > other.rk or (self.rk == other.rk and self.st > other.st):
            return True
        else:
            return False

    def __ge__(self, other):
        if self.rk >= other.rk or (self.rk == other.rk and self.st >= other.st):
            return True
        else:
            return False

    def _next(self):
        '''Returns a new Card object that is "next" in this order:
        2 of Clubs, 3 of Clubs, ..., King of Clubs, Ace of Clubs,
        2 of Diamonds, ..., Ace of Hearts, 2 of Hearts, ..., Ace of Hearts,
        2 of Spades, ..., Ace of Spades, Red Joker, Black Joker, [repeats]
                 when using empty constructor Card(), BJ ^ is the default card
        '''
        if self.st <= Suit('S'):
            if self.rk < Rank('A'):
                r, s = str(self.rk._next()), str(self.st)
            elif self.rk == Rank('A'):
                if self.st < Suit('S'):
                    r, s = '2', str(self.st._next())
                elif self.st == Suit('S'):
                    r, s = 'Z', 'B'
                # no else due to highest level `if` capturing this logic
            else: # e.g. Joker of Spades
                raise CardError(f"Invalid Card: r={self.rk}, s={self.st}")
        elif self.st == Suit('B') and self.rk == Rank('Z'):
            r, s = 'Z', 'R'
        elif self.st == Suit('R') and self.rk == Rank('Z'):
            r, s = '2', 'C'
        else: # e.g. Seven of Black
            raise CardError(f"Invalid Card: r={self.rk}, s={self.st}")
        return Card(r, s)

    def next_n(self, n): # excludes self; returns list; Card().next_n(52)
        card = self
        card_list = []
        for _ in range(n):
            card = card._next()
            card_list.append(card)
        return card_list

    def url(self, show_back=False):
      if show_back:
          return "https://raw.githubusercontent.com/chrhyman/pycards/main/assets/cards/cardback.png"
      return f"https://raw.githubusercontent.com/chrhyman/pycards/main/assets/cards/{self.rk.rank_name.lower()}_{self.st.suit_name.lower()}.png"
