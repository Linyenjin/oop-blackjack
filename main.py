import pygame

try:
    import simplegui
except ImportError:
    import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

import random
import pandas as pd

from card import Card
from hand import Hand
from deck import Deck

pygame.init()

columns = ['event', 'score', 'in_play']
data = pd.DataFrame(columns=columns)

sound_effect = pygame.mixer.Sound('bgm.mp3')
sound_effect.play()

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

def save_data(event):
    global data, score, in_play

    new_data = pd.DataFrame({ 'event': [event], 'score': [score], 'in_play': [in_play]})
    data = pd.concat([data, new_data], ignore_index=True)



# define globals for cards
def deal():
    global outcome, in_play, game_deck, player_hand
    global dealer_hand, message, display_hole_card, game_stop, score
    
    if game_stop == False:
        outcome = "You lose."
        score -= 1
        message = "New deal?"
        display_hole_card = True
        game_stop = True
                
    else:
        game_deck = Deck()
        game_deck.shuffle()

        player_hand = Hand()
        dealer_hand = Hand()

        for i in range(2):
            player_hand.add_card( game_deck.deal_card() )
            dealer_hand.add_card( game_deck.deal_card() )    

        in_play = True
        display_hole_card = False
        outcome = ""
        message = "Hit or Stand?"

        game_stop = False
        save_data("deal")

   
def hit():

    global outcome, score, message, display_hole_card, game_stop
        
    if game_stop == False:
          
        if in_play:
            if player_hand.get_value() <= 21:
                player_hand.add_card(game_deck.deal_card())

            if player_hand.get_value() > 21:
                outcome = "You went bust and lose."
                message = "New deal?"
                score -= 1
                display_hole_card = True
                game_stop = True
        else:
            dealer_hand.add_card(game_deck.deal_card())
        save_data("hit")
        
def stand():

    global in_play, outcome, score, message, display_hole_card, game_stop
    
    if game_stop == False:

        message = "New deal?"
        in_play = False

        display_hole_card = True

        while (dealer_hand.get_value() < 17):
            hit()

        if dealer_hand.get_value () > 21:
            outcome = "You won."
            score += 1

        else:
            if player_hand.get_value() <= dealer_hand.get_value():
                outcome = "You lose."
                score -= 1        

            else:
                outcome = "You won."
                score += 1
            save_data("stand")

        game_stop = True

def draw(canvas):
    
    # draw title
    canvas.draw_text("Blackjack", [100, 100], 50,  "Red")
    canvas.draw_text("Score: " + str(score), [400, 100], 40,  "yellow")
    
    # draw dealer and player
    canvas.draw_text("Dealer", [40, 200], 40,  "Black")      
    canvas.draw_text("Player", [40, 400], 40,  "Black")                                       
    
    # draw outcome
    canvas.draw_text(outcome, [250, 200], 35,  "Black")                                       
    canvas.draw_text(message, [300, 400], 40,  "Black")                                       
    
    # draw hands
    player_hand.draw(canvas, [50, 440])
    dealer_hand.draw(canvas, [50, 230])
    
    # draw dealer's hole card
    if display_hole_card == False:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE
                          , [50 + CARD_CENTER[0], 230 + CARD_CENTER[1]], CARD_BACK_SIZE)

def get_hand_value(hand):
    value = sum([card.get_value() for card in hand])
    has_ace = any(card.rank == 'A' for card in hand)
    if has_ace and value + 10 <= 21:
        value += 10
    return value

def save_to_csv():
    global data
    data.to_csv('game_data.csv', index=False)
    print("Data saved to game_data.csv")



# create frame and add a button and labels    
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

# register event handlers
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_button("Save Data", save_to_csv, 200)
frame.set_draw_handler(draw)

# initialize global variables
game_deck = Deck()
player_hand = Hand()
dealer_hand = Hand()

# get things rolling
deal()
frame.start()