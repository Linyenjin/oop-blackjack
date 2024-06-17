import pygame
try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

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

class Hand:
    def __init__(self):
        self.cards_list = []

    def __str__(self):
        ans = "Hand contains "
        for x in self.cards_list:
            ans += str(x) + " "
            
        return ans

    def add_card(self, card):
        self.cards_list.append(card)	

    def get_value(self):
        
        value = 0
        has_rank = False
        
        for x in self.cards_list:
            r = x.get_rank()
            
            if r == RANKS[0]:
                has_rank = True
                
            value += VALUES[r]

        if has_rank and (value+10 <= 21):
            value += 10
        
        return value
    
    
    def draw(self, canvas, pos):
        for x in self.cards_list:
            x.draw(canvas, pos)
            pos[0] += 100