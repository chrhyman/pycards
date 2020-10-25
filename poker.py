from card import Rank, Suit, Card
from deck import Deck, Hand

class PokerError(Exception):
  pass

class Poker:
    def __init__(self):
        self.hand = Hand("Player")
        self.deck = Deck(Card().next_n(52))
        self.deck.shuffle()
        self.win_str = None

    def deal(self):
        self.__init__()
        self.deck.deal_n(self.hand, 5)

    def draw(self, keep_list):
        if len(keep_list) != 5:
            raise PokerError(f"Invalid keep_list: {keep_list}")
        if len(self.hand) != 5:
            raise PokerError(f"Invalid Hand: {repr(self.hand)}")
        for i, keep_card in enumerate(keep_list):
            if not keep_card:
                self.deck.shuffle()
                self.hand[i] = self.deck.pop()
        return self._calculate_win()

    def _calculate_win(self): # returns int mult for bet, updates self.win_str
        pays = {'Royal Flush': 800, 'Straight Flush': 50, 'Four of a Kind': 25,
                'Full House': 9,'Flush': 6, 'Straight': 4, 'Three of a Kind': 3,
                'Two Pair': 2, 'Jacks or Better': 1, 'Try again': 0}
        best_hand = 'Try again'
        cards = sorted(self.hand) # copy so it doesn't affect display order
        ranks = [c.rank_i for c in cards]
        suits = [c.suit_i for c in cards]
        flags = {'Royal Flush': False, 'Straight Flush': False,
                'Four of a Kind': False, 'Full House': False,'Flush': False,
                'Straight': False, 'Three of a Kind': False, 'Two Pair': False,
                'Jacks or Better': False, 'pair': False}
        # pair (unused for wins)
        # jacks or better = pair and rank in pair is >= Rank('J')
        # two pair
        # three of a kind
        # straight
        # flush
        # full house = three of a kind and pair
        # four of a kind
        # straight flush = straight and flush
        # royal flush = straight and flush and max Card Rank == Rank('A')
        is_flush = True if len(set(suits)) == 1 else False
        # check for straight
        #
        #
        self.win_str = best_hand
        return pays[best_hand]

    def get_hand(self):
        return repr(self.hand)

    def get_win(self, credits_won):
        if credits_won > 0:
            return f"{self.win_str}! +{credits_won} credits"
        else:
            return self.win_str

    def load(self, hand_repr):
        card_list = hand_repr.split(',')
        cards = []
        for card_str in card_list:
            rank, suit = card_str.split('.')
            cards.append(Card(rank, suit))
        self.__init__()
        for card in cards:
            self.deck.deal_card(self.hand, card)
