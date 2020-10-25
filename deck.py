from random import shuffle

class Deck(list):
    def __repr__(self): # "A.C,T.S,K.H" = Deck([Card('A', 'C'), Card('T', 'S'), Card('K', 'H')])
        return ",".join(repr(c) for c in self)

    def __str__(self): # Ace of Clubs, Ten of Spades, King of Hearts
        return ", ".join(str(c) for c in self)

    def deal_n(self, player_hand, n):
        for _ in range(n):
            player_hand.append(self.pop())

    def deal_card(self, player_hand, card):
        player_hand.append(self.pop_card(card))

    def pop_card(self, card):
        return self.pop(self.index(card))

    def shuffle(self):
        shuffle(self)

class Hand(Deck):
    def __init__(self, name, cards=[]):
        self.name = name
        super().__init__(cards)
