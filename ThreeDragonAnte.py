import random, time, os
from variables import name_list, deck_list
from collections import Counter
clear = lambda: os.system('clear')

# *** Add player turns beginning with the round leader ***
# Review order_by_str function
# when choosing a card, allow player to sort hand by type or str with commands
# track next_round_leader for highest played str
# Change Print statements that as the use if they are ready to procede after each screen, for cleaner printing and readibility


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

# Create basic Deck list for phase one of code writing
refactored_list = []
for i in range(len(deck_list)):
  card_strength = int(deck_list[i][-2:].strip())
  refactored_list.append([deck_list[i], card_strength])

deck_list = refactored_list
draw_pile = deck_list
discard_pile = []
ante_pile = []

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
    self.cards_played_this_gambit = []

  def __repr__(self):
    return self.name

  def draw(self, num):
    print(f"{self.name} draws {num} card(s)")
    # With Colors
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

  def order_by_str(self):
    self.hand = self.hand.sort()

  def choose_card(self):
    
    # Add functionality for additional sorting commands
    card_chosen = False
    while not card_chosen:
      print("YOUR HAND:")
      for i, card in enumerate(self.hand, 1):
        print(f"  {i}. {card[0]}")
      
      acceptable_inputs = range(1, self.hand_size + 1)
      #acceptable_inputs += [other functions here like ordering list by str or type]
      
      card_index = None
      while card_index not in acceptable_inputs:
        card_index = input(f"Enter the card number you want to ante (1-{self.hand_size}): ")
        try:
          card_index = int(card_index)
          card_chosen = True
        except ValueError:
          # CHECK ADDITIONAL FUNCTIONS
          # if card_index in acceptable_inputs:
          #   pass
          print("Please enter a valid number.")
          card_index = None
    
    chosen_card = self.hand[card_index - 1]
    return chosen_card

  def ante_card(self):
    ante_card = self.choose_card()
    self.hand.remove(ante_card)
    return [self, ante_card]
  
  def main_turn(self,last_str_played=None):
    print(f"\n--------------- PLAYER TURN ---------------")
    # Print Hand
    card_to_play = self.choose_card()
    # if card_to_play[1] >= last_str_played:
    #   power_activates = True
    #   card.call_effect
    self.flight.append(card_to_play)
    self.hand.remove(card_to_play)

class Player():

  def __init__(self, player_id, name, hand, starting_gold):
    self.id = player_id
    self.name = name
    self.hand = hand
    self.gold = starting_gold
    self.hand_size = len(hand)
    self.flight = []
    self.cards_played_this_gambit = []

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
  
  def main_turn(self, last_str_played=None):
    # determine_strategy() function

    # plays strongest cards
    # Determine strongest
    self.strongest_card = self.hand[0]
    for item in self.hand:
      if item[1] > self.strongest_card[1]:
        self.strongest_card = item
    # Add to flight, remove from hand
    self.card_to_play = self.strongest_card
    self.flight.append(self.card_to_play)
    self.hand.remove(self.card_to_play)
    print(f"{self} plays {self.card_to_play[0]} ")

# --------------------------------------
# --------------------------------------
# --------------------------------------

#Functions
def shuffle_deck():
  random.shuffle(draw_pile)
  print("Deck was shuffled.")

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
  global round_leader, gambit_number, player_list#, highest_card_so_far
  gambit_number += 1
  print(f"START GAMBIT {gambit_number}")
  time.sleep(2)
  clear()
  print("--------------- PLAYER ANTE ---------------")
  # ANTE PHASE RETURNS A PLAYER CLASS, GOLD
  round_leader, ante_gold = ante_phase()
  print(f"\nEach player antes {ante_gold} gold.\n{round_leader} will start the round.")
  time.sleep(2)
  print_board()

  highest_card_so_far = None
  # Each player
  for i in range(rounds_in_gambit):
    # Build a reordered list starting from the round leader
    leader_index = player_list.index(round_leader)
    ordered_players = player_list[leader_index:] + player_list[:leader_index]

    for player in ordered_players:
      player.main_turn()
    print_board()

# --------------------------------------
# --------------------------------------
# --------------------------------------    

# ---------- Number of Players ----------
player_count = None
while player_count not in ["2","3","4","5","6", ""]:
  player_count = input("How many players will there be? (2-6): ")
  if player_count == "":
    player_count = "2"
player_count = int(player_count)
clear()

# ---------- Player Names ----------
#print("Choosing player names . . .")
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
#print("Dealing starting hands . . .")
hand_lists = []
for i in range(player_count):
  player_hand = []
  for i in range(6):
    card = draw_pile.pop()
    player_hand.append(card)
  hand_lists.append(player_hand)

# ---------- Initialize Classes ----------
#print("Calculating starting gold . . .")
starting_gold = 10 * player_count
player_list = []

#print("Initializing player classes . . .")
# USER CLASS
player_list.append(User(0, player_names_list[0], hand_lists[0], starting_gold))

# Computer classes
for i in range(player_count - 1):
  player_list.append(Player(i+1, player_names_list[i+1], hand_lists[i+1], starting_gold))

# ---------- Additional Variables ----------
#print("Setting final game variables . . .\n")
stakes = 0
round_leader = None
gambit_number = 0
round_number = 0
highest_card_so_far = None
rounds_in_gambit = 3

# ---------- Start Game ----------
start_gambit()


