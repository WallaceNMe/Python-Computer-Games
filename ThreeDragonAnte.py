import random, time, os
from variables import name_list, deck_list
from collections import Counter
clear = lambda: os.system('clear')

GREEN_BG = '\033[42m\033[30m\033[1m'
YELLOW_BG = '\033[43m\033[30m\033[1m'
GRAY_BG = '\033[100m\033[37m\033[1m'
RESET = '\033[0m'

refactored_list = []
for i in range(len(deck_list)):
  card_strength = int(deck_list[i][-2:].strip())
  refactored_list.append([deck_list[i], card_strength])

deck_list = refactored_list
draw_pile = deck_list
discard_pile = []
use_pile = []
ante_pile = []
my_var_ref = {}

# --------------------------------------
# --------------------------------------
# --------------------------------------

#Classes

class Player():

  # ----- VAR lIST -----
  # self.id = 0-5
  # self.name = "My Name"
  # self.hand = [["Silver 4", [4]], ["Green 5", 5]]
  # self.gold = 20-60
  # self.hand_size = len(hand)
  # self.flight = [["Silver 4", [4]], ["Green 5", 5]]

  def __init__(self, player_id, name, hand, starting_gold):
    self.id = player_id
    self.name = name
    self.hand = hand
    self.gold = starting_gold
    self.hand_size = len(hand)
    self.flight = []

  def __repr__(self):
    return self.name

  def draw(self, num):
    for i in range(num):
      new_card = draw_pile.pop()
      self.hand.append(new_card)
      check_reshuffle()
    if num == 1:
      print(f"{self.name} draws {num} card")
    elif num > 1:
      print(f"{self.name}  draws {num} cards")
    else:
      print("CARD NUM PRINT ERROR")

  def pay_gold(self, amount):
    self.gold -= amount

  def ante_card(self):
    #Ante lowest str card
    self.card_to_ante = self.hand[0]
    for i in range(len(self.hand)):
      if self.hand[i][1] < self.card_to_ante[1]:
        self.card_to_ante = self.hand[i]

    # Remove from player hand and return card and the player it came from
    self.hand.remove(self.card_to_ante)
    return [self, self.card_to_ante]
  
  def main_turn(self):
    pass
    
# --------------------------------------
# --------------------------------------
# --------------------------------------

#Functions
def shuffle_deck():
  random.shuffle(draw_pile)
  print("Deck was shuffled.")

def print_ref():
  global my_var_ref
  print("my_var_ref:")
  print('\n'.join(GREEN_BG + f"{key}" + RESET + f": {value}" for key, value in my_var_ref.items()))

def check_reshuffle():
  global draw_pile
  if len(draw_pile) == 0:
    # Copy adds insurance
    draw_pile = discard_pile.copy()
    discard_pile = []
    shuffle_deck()

def ante_phase():
  global stakes, current_round_leader
  
  acceptable_ante = False
  while not acceptable_ante:
    # Retrieve Ante Cards
    returned_list = []
    for i in range(len(player_list)):
      # Returns [Player Class, [Card, STR]]
      returned_list.append(player_list[i].ante_card())
    
    # Print ante results
    for i in range(len(returned_list)):
      print(f"{returned_list[i][0]} antes: {returned_list[i][1][0]}")
    #print(returned_list)
  
    # ----- Check Edge Case -----

    # Get all strength values
    strength_values = [return_value[1][1] for return_value in returned_list]
    
    # Check if all cards have the same strength (all tied)
    if len(set(strength_values)) == 1:
      print("\nAll ante cards were tied, Each player Draws a card and re-antes.\n")
      time.sleep(1)
      for return_value in returned_list:
        # Discard ante cards
        discard_pile.append(return_value[1])
        # Draw 1
        return_value[0].draw(1)
    # Re-ante
    else:
      acceptable_ante = True
  
  # ----- Resume Ante -----

  ante_pile = [return_value[1] for return_value in returned_list]

  # Find the highest strength card
  highest_str_value = max(strength_values)
  highest_str_return = [r for r in returned_list if r[1][1] == highest_str_value][0]
  
  # Deduct gold from each player equal to highest_str_value
  for player in player_list:
    player.pay_gold(highest_str_value)
    stakes += highest_str_value
  
  # ----- Determine First Player -----
  
  # Count occurrences of each strength value
  strength_counts = Counter(strength_values)
  
  # Keep only untied values
  untied_values = [value for value, count in strength_counts.items() if count == 1]
  
  # If an untied card was played
  if untied_values:
    # Find the highest untied value
    highest_untied = max(untied_values)
    # Find the player who played that card
    first_player = [r[0] for r in returned_list if r[1][1] == highest_untied][0]
  else:
    # All cards are tied - use previous round's leader or default
    if current_round_leader:
        first_player = current_round_leader
    else:
        # First round and all tied - random selection
        print("All cards are tied, so the first player will be random.")
        first_player = random.choice(player_list)
        print(f"The first player will be {first_player}")
    
  
  return first_player

def start_gambit():
  current_round_leader = ante_phase()
  print(f"\n{current_round_leader} will start the round.\n")

  # ANTE PHASE RETURNS A PLAYER CLASS

# --------------------------------------
# --------------------------------------
# --------------------------------------    

# ---------- Number of Players ----------
player_count = 0
while player_count not in ["2","3","4","5","6", ""]:
  player_count = input("How many players will there be? (2-6): ")
  if player_count == "":
    player_count = "2"
player_count = int(player_count)
clear()

# ---------- Player Names ----------
user_name = "Player 1"
player_names_list = [user_name]
num = 1
for i in range(player_count):
  num += 1
  player_names_list.append(f"Player {num}")
# FOR ACTUAL NAMES:
# user_name = input("Enter your character's name: ")
# if user_name == "":
#   user_name = "TEST_USER"

# player_names_list = []
# player_names_list.append(user_name)
# for i in range(5):
#   name = random.choice(name_list)
#   name_list.remove(name)
#   player_names_list.append(name)

# ---------- Starting Hand ----------
shuffle_deck()
hand_lists = []
for i in range(player_count):
  player_hand = []
  for i in range(6):
    card = draw_pile.pop()
    player_hand.append(card)
    use_pile.append(card)
  hand_lists.append(player_hand)

# ---------- Initialize Classes ----------
starting_gold = 10 * player_count
player_list = []
for i in range(player_count):
  player_list.append(Player(i, player_names_list[i], hand_lists[i], starting_gold))
  my_var_ref[f"Player {i}'s hand"] = hand_lists[i]

#------------------------------------------
my_var_ref["player_count"] = player_count
my_var_ref["user_name"] = user_name
my_var_ref["player_names_list"] = player_names_list
my_var_ref["starting gold"] = starting_gold
my_var_ref["use_pile"] = use_pile
my_var_ref["hand_lists (starting)"] = hand_lists
#print_ref()

# --------------------------------------
# --------------------------------------
# --------------------------------------

# Start Game
stakes = 0
current_round_leader = None

start_gambit()

