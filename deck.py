from random import shuffle

class Deck(list):
    def __repr__(self):
        return f'''Deck([{", ".join(repr(c) for c in self)}])'''

    def __str__(self):
        return ", ".join(str(c) for c in self)

    def deal_n(self, hand, n):
        for _ in range(n):
            hand.append(self.pop())

    def deal_card(self, hand, card):
        hand.append(self.pop_card(card))

    def pop_card(self, card):
        return self.pop(self.index(card))

    def shuffle(self):
        shuffle(self)

    def top_n(self, n):
        next_cards = []
        for i in range(n):
            next_cards.append(self[-(i + 1)])
        return next_cards

class Hand(Deck):
    def __init__(self, name, cards=[]):
        self.name = name
        super().__init__(cards)

    def __repr__(self):
        return f'''Hand("{self.name}", [{", ".join(repr(c) for c in self)}])'''
