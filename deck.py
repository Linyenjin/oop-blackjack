import pygame
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

from card import Card

CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    


# initialize some useful global variables
in_play = False
outcome = ""
score = 0
message = ""
display_hole_card = False
game_stop = True

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

class Deck:
    def __init__(self):       
        self.cards_list = [Card(s,r) for s in SUITS for r in RANKS]
        
    def shuffle(self):
        random.shuffle(self.cards_list) 

    def deal_card(self):
        return self.cards_list.pop(-1)
    
    def __str__(self):
        ans = "Deck contains "
        for x in self.cards_list:
            ans += str(x) + " "
            
        return ans   