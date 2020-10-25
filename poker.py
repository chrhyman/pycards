from .card import Card
from .deck import Deck, Hand

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

    def _calculate_win(self): # returns int multiplier of the calculated win and updates self.win_str
        pays = {'Royal Flush': 800, 'Straight Flush': 50, 'Four of a Kind': 25,
                'Full House': 9,'Flush': 6, 'Straight': 4, 'Three of a Kind': 3,
                'Two Pair': 2, 'Jacks or Better': 1, 'Try again': 0}
        best_hand = 'Try again'
        cards = sorted(self.hand) # copy so it doesn't affect the internal order for displaying
        ranks = [c.rank_i for c in cards]
        suits = [c.suit_i for c in cards]
        # check for flush
        is_flush = True if len(set(suits)) == 1 else False
        # check for straight
        #
        #
        self.win_str = best_hand
        return pays[best_hand]

    def get_hand(self):
        return repr(self.hand)

    def get_win(self, credits_won):
        # do something with credits_won
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
