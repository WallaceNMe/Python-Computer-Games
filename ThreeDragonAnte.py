import random, time, os
from variables import name_list, deck_list
from collections import Counter
clear = lambda: os.system('clear')


# Begin working on player main turn
# track next_round_leader for highest played str


GREEN_BG = '\033[42m\033[30m\033[1m'
YELLOW_BG = '\033[43m\033[30m\033[1m'
GRAY_BG = '\033[100m\033[37m\033[1m'
RESET = '\033[0m'

# Background colors with black text and bold
RED_BG = '\033[41m\033[30m\033[1m'
BLUE_BG = '\033[44m\033[30m\033[1m'
MAGENTA_BG = '\033[45m\033[30m\033[1m'
CYAN_BG = '\033[46m\033[30m\033[1m'
WHITE_BG = '\033[47m\033[30m\033[1m'

# Bright background colors with black text and bold
BRIGHT_RED_BG = '\033[101m\033[30m\033[1m'
BRIGHT_GREEN_BG = '\033[102m\033[30m\033[1m'
BRIGHT_YELLOW_BG = '\033[103m\033[30m\033[1m'
BRIGHT_BLUE_BG = '\033[104m\033[30m\033[1m'
BRIGHT_MAGENTA_BG = '\033[105m\033[30m\033[1m'
BRIGHT_CYAN_BG = '\033[106m\033[30m\033[1m'
BRIGHT_WHITE_BG = '\033[107m\033[30m\033[1m'

# If you need white text instead of black on darker backgrounds
BLUE_BG_WHITE = '\033[44m\033[37m\033[1m'
RED_BG_WHITE = '\033[41m\033[37m\033[1m'
MAGENTA_BG_WHITE = '\033[45m\033[37m\033[1m'

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
class User():
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
    print(f"{self.name} draws {num} card(s)")
    # if num == 1:
    #   print(BLUE_BG_WHITE + f"{self.name} draws {num} card" + RESET)
    # elif num > 1:
    #   print(BLUE_BG_WHITE + f"{self.name}  draws {num} cards" + RESET)
    # else:
    #   print(RED_BG + "CARD NUM PRINT ERROR" + RESET)
    for i in range(num):
      new_card = draw_pile.pop()
      self.hand.append(new_card)
      check_reshuffle()
      print(f"You have drawn: {new_card[0]}{RESET}")    

  def receive_gold(self, amount):
    self.gold += amount

  def pay_gold(self, amount, to_player=None):
    self.gold -= amount
    if to_player:
      to_player.receive_gold(amount)

  def print_status(self):
      if self == round_leader:
        print(f"{self} {CYAN_BG}(RL){RESET}: {self.gold}GP, {self.hand_size} Cards")
      else:
        print(f"{self}: {self.gold}GP, {self.hand_size} Cards")
      # reformat flight for printing
      flight_reformatted = [value[0] for value in self.flight]
      print(f"  Flight: {', '.join(flight_reformatted)}")

  def ante_card(self):
    print("YOUR HAND:")
    for i, card in enumerate(self.hand, 1):
      print(f"  {i}. {card[0]}")
    
    card_index = None
    while card_index not in range(1, self.hand_size + 1):
      try:
        card_index = int(input(f"Enter the card number you want to ante (1-{self.hand_size}): "))
      except ValueError:
        print("Please enter a valid number.")
        card_index = None
    
    card_to_ante = self.hand[card_index - 1]
    self.hand.remove(card_to_ante)
    return [self, card_to_ante]
    
    # #Ante lowest str card
    # self.card_to_ante = self.hand[0]
    # for i in range(len(self.hand)):
    #   if self.hand[i][1] < self.card_to_ante[1]:
    #     self.card_to_ante = self.hand[i]

    # # Remove from player hand and return card and the player it came from
    # self.hand.remove(self.card_to_ante)
  
  def main_turn(self,last_str_played=None):
    print(f"\n--------------- PLAYER TURN ---------------")
    # Print Hand
    print("YOUR HAND:")
    for i, card in enumerate(self.hand, 1):
      print(f"  {i}. {card[0]}")
    # Demand card to play
    card_index = None
    while card_index not in range(1, self.hand_size + 1):
      try:
        if last_str_played:
          print(f"The last card played was STR {last_str_played}")
        card_index = int(input(f"Enter the card number you want to play (1-{self.hand_size}): "))
      except ValueError:
        print("Please enter a valid number.")
        card_index = None

    card_to_play = self.hand[card_index - 1]
    self.flight.append(card_to_play)
    self.hand.remove(card_to_play)

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
    print(f"{self.name} draws {num} card(s)")
    for i in range(num):
      new_card = draw_pile.pop()
      self.hand.append(new_card)
      check_reshuffle()
    # if num == 1:
    #   print(BLUE_BG_WHITE + f"{self.name} draws {num} card" + RESET)
    # elif num > 1:
    #   print(BLUE_BG_WHITE + f"{self.name}  draws {num} cards" + RESET)
    # else:
    #   print(RED_BG + "CARD NUM PRINT ERROR" + RESEt)

  def receive_gold(self, amount):
    self.gold += amount

  def pay_gold(self, amount, to_player=None):
    self.gold -= amount
    if to_player:
      print(f"{self.name} pays {amount} gold to {to_player}.")
      to_player.receive_gold(amount)

  def print_status(self):
      if self == round_leader:
        print(f"{self} {CYAN_BG}(RL){RESET}: {self.gold}GP, {self.hand_size} Cards")
      else:
        print(f"{self}: {self.gold}GP, {self.hand_size} Cards")
      # reformat flight for printing
      flight_reformatted = [value[0] for value in self.flight]
      print(f"  Flight: {', '.join(flight_reformatted)}")

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
    # determine_strategy() function

    # plays strongest cards
    # Determine strongest
    self.strongest_card = self.hand[0]
    for item in self.hand:
      if item[1] > self.strongest_card[1]:
        self.strongest_card = item
    # Add to flight, remove from hand
    self.flight.append(strongest_card)
    self.hand.remove(strongest_card)

    
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

def print_board():
  global stakes, round_leader, ante_pile
  print("\n--------------- TABLE VIEW ---------------")
  print(f"Stakes: {stakes}")
  reformatted_ante = [value[0] for value in ante_pile]
  print(f"Ante: {", ".join(reformatted_ante)}")
  for player in player_list:
    player.print_status()
  #print("------------------------------")

def ante_phase():
  global stakes, round_leader, ante_pile
  
  acceptable_ante = False
  while not acceptable_ante:
    # Retrieve Ante Cards
    returned_list = []
    for i in range(len(player_list)):
      # Returns [Player Class, [Card, STR]]
      returned_list.append(player_list[i].ante_card())
    
    # Print ante results
    print("\n--------------- ANTE PHASE ---------------")
    # Print Player Antes
    for i in range(len(returned_list)):
      print(f"{returned_list[i][0]} antes: {returned_list[i][1][0]}")

    # ----- Check All Tied (Re-ante) -----

    # Get all strength values
    strength_values = [return_value[1][1] for return_value in returned_list]
    
    # Check if all cards have the same strength (all tied)
    if len(set(strength_values)) == 1:
      print("\n**All ante cards were tied, Each player draws a card and re-antes.**\n")
      for return_value in returned_list:
        # Discard ante cards
        discard_pile.append(return_value[1])
        # Draw 1
        return_value[0].draw(1)
    # Re-ante
    else:
      acceptable_ante = True
  
  # ----- Resume Ante -----

  # Add cards to ante_pile
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
    # All cards are tied with at least one other card - use previous round's leader or default
    if round_leader:
        first_player = round_leader
        print("The previous round leader will start the next gambit.")
    else:
        # First round and all tied - random selection
        print("All cards are tied with at least one other, so the first player will be random.")
        first_player = random.choice(player_list)
        print(f"The first player will be {first_player}")
    
  
  return first_player, highest_str_value

def start_gambit():
  global round_leader, gambit_number
  gambit_number += 1
  print(f"BEGIN GAMBIT {gambit_number}")
  print("--------------- PLAYER ANTE ---------------")
  # ANTE PHASE RETURNS A PLAYER CLASS
  round_leader, ante_gold = ante_phase()
  print(f"\nEach player antes {ante_gold} gold.\n{round_leader} will start the round.")
  time.sleep(2)
  print_board()

  highest_str_card_player = None
  # Each player 

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
  player_names_list.append(f"Computer {num}")
# ----- FOR ACTUAL NAMES -----
# user_name = input("Enter your character's name: ")
# if user_name == "":
#   user_name = "TEST_USER"

# player_names_list = []
# player_names_list.append(user_name)
# for i in range(5):
#   name = random.choice(name_list)
#   name_list.remove(name)
#   player_names_list.append(name)

# ---------- Starting Hands ----------
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

# USER CLASS
player_list.append(User(0, player_names_list[0], hand_lists[0], starting_gold))
my_var_ref[f"User's Hand"] = hand_lists[0]

# Computer classes
for i in range(player_count - 1):
  player_list.append(Player(i+1, player_names_list[i+1], hand_lists[i+1], starting_gold))
  my_var_ref[f"Player {i}'s hand"] = hand_lists[i]

# ---------- Variable Reference ----------
my_var_ref["player_count"] = player_count
my_var_ref["user_name"] = user_name
my_var_ref["player_names_list"] = player_names_list
my_var_ref["starting gold"] = starting_gold
my_var_ref["use_pile"] = use_pile
my_var_ref["hand_lists (starting)"] = hand_lists

# ---------- Additional Variables ----------
stakes = 0
round_leader = None
gambit_number = 0

# ---------- Start Game ----------
start_gambit()
