from random import shuffle

class Deck(list):
    def __repr__(self): # "A.C,Z.B" = Deck([Card('A', 'C'), Card('Z', 'B')])
        return ",".join(repr(c) for c in self)

    def __str__(self): # above example = Ace of Clubs, Black Joker
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
