from card import Rank, Suit, Card, RankError
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
        # dict paytable
        pays = {'Royal Flush': 800, 'Straight Flush': 50, 'Four of a Kind': 25,
                'Full House': 9,'Flush': 6, 'Straight': 4, 'Three of a Kind': 3,
                'Two Pair': 2, 'Jacks or Better': 1, 'Try again': 0}
        best_hand = 'Try again'
        cards = sorted(self.hand) # copy so it doesn't affect display order
        flags = {'Flush': False, 'Straight': False}
        freq_count = {} # {'rank': int count of occurrences of rank in hand}
        for card in cards:
            if str(card.rk) in freq_count:
                freq_count[str(card.rk)] += 1
            else:
                freq_count[str(card.rk)] = 1
        freqs = [freq_count[k] for k in freq_count] # list of frequency values
        # set best_hand in order so that it is overwritten as hands improve
        if 2 in freqs:
            for rank in freq_count:
                if Rank(rank) >= Rank('J') and freq_count[rank] == 2:
                    best_hand = 'Jacks or Better'
            if freqs.count(2) == 2:
                best_hand = 'Two Pair'

        if 3 in freqs:
            best_hand = 'Three of a Kind'

        straight_check_from = Rank(min(cards).rk.rank)
        if Rank('A') in cards:
            straight_check_from = Rank('A')
            if Rank('T') in cards:
                straight_check_from = Rank('T')
        try:
            straight_check = straight_check_from.run_of(5)
            flags['Straight'] = all([rank in cards for rank in straight_check])
        except RankError:
            flags['Straight'] = False
        if flags['Straight']:
            best_hand = 'Straight'

        num_suits = len(set([c.st.suit for c in cards]))
        if num_suits == 1:
            flags['Flush'] = True
            best_hand = 'Flush'

        if 3 in freqs and 2 in freqs:
            best_hand = 'Full House'

        if 4 in freqs:
            best_hand = 'Four of a Kind'

        if flags['Straight'] and flags['Flush']:
            best_hand = 'Straight Flush'
            if Rank('T') in cards and Rank('A') in cards:
                best_hand = 'Royal Flush'

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
