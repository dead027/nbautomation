#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2023/6/1 15:22
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from collections import namedtuple, deque
from random import shuffle
from Library.LiveLibrary.PublicVariables import order_value_dic


poker = namedtuple("Pokers", ["color", "colorValue", "originNumber", "naturalNumber", "singleNumber"])
colors = ["Spades", "Hearts", "Clubs", "Diamonds"]


class PokerSuite(object):
    def __init__(self, multiple=1):
        self.multiple = multiple
        self.cards = deque()
        self.shuffle_suite()

    def __len__(self):
        return self.cards.__len__()

    @staticmethod
    def __create_cards(multiple):
        suite = deque()
        for color in colors:
            for number in range(1, 14):
                if number == 1:
                    suite.append(poker(color, 4 - colors.index(color), 'A', number, 1))
                elif number <= 10:
                    suite.append(poker(color, 4 - colors.index(color), order_value_dic[number], number, number))
                else:
                    suite.append(poker(color, 4 - colors.index(color), dict(zip(range(11, 14), 'JQK'))[number], number,
                                       0))
        suite *= multiple
        return suite

    def get_cards(self, card_count, if_new=False, direct="up"):
        assert direct in ['up', 'down']
        card_count = int(card_count)
        if self.__len__() < card_count or if_new:
            self.shuffle_suite()
        return [self.cards.pop() if direct == 'up' else self.cards.popleft() for _ in range(card_count)]

    def shuffle_suite(self):
        self.cards = self.__create_cards(self.multiple)
        shuffle(self.cards)

    def get_cards_of_str(self, card_count, if_new=True):
        return ','.join([f"{item.colorValue}{item.originNumber}" for item in self.get_cards(int(card_count), if_new)])


if __name__ == "__main__":
    p = PokerSuite(1)
    print(p.get_cards(6))
