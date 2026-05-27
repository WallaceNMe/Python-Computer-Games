import random, os, sys
from gamestate import g
from classes import User, Player
from functions import print_special_card_options, proceed, print_traditional, ten_random, print_random_ten, shuffle_deck, gambit, clear

from collections import Counter


# LINE 366 OF FUNCTIONS REFORMAT SO THE 'V' VIEW DISPLAYS PROPER COLORS INSTEAD OF JUST ALL GRAY.
# Refactor player.choose_card() - Header specifically
# Go through everything start to finish



# --------------------------------------
# ---------------- NOTES ---------------
# --------------------------------------

# Add card powers - Refactor as Class
# Add check_stakes function to end gambit
# Add something for a Fellowship
# Power always activates for Legendary Dragons

# Later
# -----
# No gold in stakes: gambit ends immediately
# Players cannot steal negative into the stakes
# Remove enter for player choice and player number auto select
# Remove draw 3 cards feature in gambit.
# Auto Choose str ante cards.

# When players choose card options, each archetype should have a few favorite cards they want in the deck that they will choose from.
# Check all places where draw_pile.pop() is called. Make sure there is a check_reshuffle() after it. 
# Check all things pull from draw_pile instead of deck_list
# Compile a README or game manual that prints at the start of the game. Include choose card commands
# Draw() prints "You have drawn X". Is that ok for round events/progression.
# Computers that will steal cards will take the last or first card in the player's hand to try and get a high card. Players can shuffle their hands before choosing which card to give up to avoid this. 

# --------------------------------------
# ------------- INITIALIZE -------------
# --------------------------------------    

# ---------- Number of Players ----------
while g.player_count not in ["2","3","4","5","6", ""]:
  g.player_count = input("How many players will there be? (2-6): ")
  # TESTING
  if g.player_count == "":
    g.player_count = "2"
g.player_count = int(g.player_count)
clear()

# ---------- Player Names ----------
# Player
player_names_list = []
g.user_name = "Player 1"
player_names_list.append(g.user_name)
# Computer
num = 1
for i in range(g.player_count):
  num += 1
  player_names_list.append(f"Player {num}")

# ----- FOR ACTUAL NAMES -----
# g.user_name = input("Enter your character's name: ")

# player_names_list.append(g.user_name)
# for i in range(5):
#   name = random.choice(g.name_list)
#   g.name_list.remove(name)
#   player_names_list.append(name)

# ---------- Card Deck ----------

print_special_card_options()

# Acceptable input
chosen_method = None
while chosen_method not in ["1", "2", "3", "4", ""]:
  chosen_method = input("Enter #: ")
  if chosen_method == 'v':
    print_traditional()
    clear()
    print_special_card_options()

if chosen_method in ["", "4"]:
  # Traditional
  g.picked_cards = g.traditional_mortals_list
elif chosen_method == "1":
  # --- Pick 'em ---
  # Each player chooses one
  clear()
  # PRINT OPTIONS
  counter = 1
  mortals_reformatted = [f"{g.GRAY_BG}{card}{g.RESET} - {card.power}" for card in g.mortals_list]
  special_dragons_reformatted = [f"{g.GRAY_BG} {card} [{card.alignment}]{g.RESET} - {card.power}" for card in g.special_dragons_list]

  print(f"{g.user_name}, make your choice:")
  print(f"{g.BRIGHT_MAGENTA_BG}----- MORTALS -----{g.RESET}") 
  for line in mortals_reformatted:    
    print(f"{counter}.) {line}")
    counter += 1
  print(f"{g.YELLOW_BG}----- SPECIAL DRAGONS -----{g.RESET}")
  for line in special_dragons_reformatted:
    print(f"{counter}.) {line}")
    counter += 1
  
  # Acceptable response
  card_choice = None
  while card_choice not in range(1, counter):
    try:
      card_choice = int(input("Enter your selection: "))
    except ValueError:
      pass

  if card_choice in range(1, len(g.mortals_list) + 1):
    # Mortals
    chosen_card = g.mortals_list[card_choice - 1]
  else:
    # Special Dragons
    index_range = range(0, (counter - len(g.mortals_list) - 1))
    chosen_card = g.special_dragons_list[index_range[card_choice - counter]]
    special_dragons_list.remove(chosen_card)

  g.picked_cards.append(chosen_card)
  clear()
  print(f"You have selected {chosen_card}.")
  proceed()

  # other players choose
  for player in range(g.player_count - 1):
    unacceptable = True
    while unacceptable:
      mortal_or_dragon = random.randint(1,2)
      if mortal_or_dragon == 1:
        other_chosen_card = random.choice(g.mortals_list)
      else:
        other_chosen_card = random.choice(g.special_dragons_list)
      if other_chosen_card not in g.picked_cards:
        unacceptable = False
    g.picked_cards.append(other_chosen_card)

  # FIll slots
  remaining = 10 - len(g.picked_cards)
  combined = [card for card in (g.mortals_list + g.special_dragons_list) if card not in g.picked_cards]
  chosen_cards = random.sample(combined, remaining)
  for card in chosen_cards:
    g.picked_cards.append(card)

elif chosen_method == "2":
  # --- Show 'em ---
  clear()
  g.picked_cards = ten_random()
  
  g.picked_cards.sort(key=lambda card: card.alignment, reverse=True)

  print_random_ten()

elif chosen_method == "3":
  # --- Among Friends ---
  clear()
  g.picked_cards = ten_random()

# Add special cards to deck
for card in g.picked_cards:
  g.deck_list.append(card)

clear()
print("Special Cards have been added to the deck.")
proceed()

# Card Lists
g.draw_pile = g.deck_list.copy()

# ---------- Init Classes ----------
# Starting Gold
g.starting_gold = 10 * g.player_count

# User class
g.player_list.append(User(player_names_list[0]))

# Computer classes
for i in range(g.player_count - 1):
  g.player_list.append(Player(player_names_list[i+1]))

# Draw
shuffle_deck()
for player in g.player_list:
  player.draw(6)

# ---------- Start Game ----------
while not g.loser:
  gambit()

clear()
print(f"{g.loser} has no more gold. Thank you for playing.")