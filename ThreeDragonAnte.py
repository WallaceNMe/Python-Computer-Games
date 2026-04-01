import random, time, os, sys
from variables import name_list, deck_list
from collections import Counter
clear = lambda: os.system('clear')


# Finished small cleanup details with printing and POWER ACTIVATES. Continue with game progression and win condition. 
# 

# Later
# Remove enter for player choice auto select
# Compile a README or game manual that prints at the start of the game. Include choose card commands
# Computers that will steal cards will take the last or first card in the player's hand to try and get a high card. Players can shuffle their hands before choosing which card to give up to avoid this. 

# COMMANDS
# 

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

# Card Lists
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

  def __repr__(self): return self.name

  def draw(self, num):
    round_events.append(f"{self.name} draws {num} card(s)")
    for i in range(num):
      new_card = draw_pile.pop()
      self.hand.append(new_card)
      check_reshuffle()
      print(f"You have drawn: {new_card[0]}{RESET}")    

  def receive_gold(self, amount): self.gold += amount

  def pay_gold(self, amount, to_player=None):
    self.gold -= amount
    if to_player:
      to_player.receive_gold(amount)

  def print_status(self, is_front_runner=False):
      # Previous Leader
      if self == round_leader:
        name_display = f"{GRAY_BG}{self}{RESET}"
      # Favored Leader
      elif is_front_runner:
        name_display = f"{BRIGHT_GREEN_BG}{self}{RESET}"
      # Regular
      else:
        name_display = f"{self}"
      
      # reformat flight for printing
      flight_reformatted = [value[0] for value in self.flight]
      
      print(f"{name_display}: {self.gold}GP, {self.hand_size} Cards")
      print(f"  Flight - {', '.join(flight_reformatted)}")

  def find_lowest_str(self):
    self.lowest_str_card = self.hand[0]
    for i in range(len(self.hand)):
      if self.hand[i][1] < self.lowest_str_card[1]:
        self.lowest_str_card = self.hand[i]
    return self.lowest_str_card

  def choose_card(self, is_ante=False, current_turn=True, last_str_played=None):

    # Acceptable Inputs
    acceptable_inputs = list(range(1, self.hand_size + 1))
    additional = ["", "sc", "s", "sh"]
    for i in additional:
      acceptable_inputs.append(i)

    # Reprints for sorting commands
    reprint_necessary = True
    while reprint_necessary:
      full_board()
      
      if is_ante:
        print("--------------- PLAYER ANTE ----------------")
      else: 
        print("--------------- PLAYER TURN ---------------")
      
      # Previous STR
      if last_str_played:
        print(f"Previously played card was STR {last_str_played}")
      # List Cards
      print("YOUR HAND:")
      for i, card in enumerate(self.hand, 1):
        print(f"  {i}. {card[0]}")
      # Commands
      print("CMD: s, sc, sh")
      
      returned_input = None
      while returned_input not in acceptable_inputs:
        chosen_card = None
        returned_input = input(f"Choose a card (1-{self.hand_size}): ")
        try:
          # If acceptable integer: card chosen
          returned_input = int(returned_input)
          if returned_input in acceptable_inputs:
            chosen_card = self.hand[returned_input - 1]
            reprint_necessary = False
          else:
            print(f"Please enter a number between 1 and {self.hand_size}.")
            returned_input = None
        except ValueError:
          # If NOT a number
          if returned_input in acceptable_inputs:
            # ENTER
            if returned_input == "":
              chosen_card = self.find_lowest_str()
              reprint_necessary = False
            # S
            elif returned_input == "s":
              self.hand.sort(key=lambda card: card[1], reverse = True)
              reprint_necessary = True
              break
            # SC
            elif returned_input == "sc":
              self.hand.sort(key=lambda card: card[0].split()[0])
              reprint_necessary = True
              break
            # SH
            elif returned_input == "sh":
              random.shuffle(self.hand)
              reprint_necessary = True
              break
          else:    
            print("Please enter a valid number or command.")
            returned_input = None
    
    # Outside choice loop
    return chosen_card

  def ante_card(self):
    ante_card = self.choose_card(True,False,False)
    self.hand.remove(ante_card)
    return [self, ante_card]
  
  def main_turn(self,last_str_played=None):
    # Choose Card
    card_to_play = self.choose_card(False, True, last_str_played)
    # Power Activates?
    if last_str_played != None:
      if card_to_play[1] <= last_str_played:
        power_activates = True
        round_events.append(f"{self} POWER ACTIVATES")
        #card.call_effect
    self.flight.append(card_to_play)
    self.hand.remove(card_to_play)
    round_events.append(f"{self} Plays {card_to_play[0]}")
    return card_to_play

class Player():

  def __init__(self, player_id, name, hand, starting_gold):
    self.id = player_id
    self.name = name
    self.hand = hand
    self.gold = starting_gold
    self.hand_size = len(hand)
    self.flight = []
    self.cards_played_this_gambit = []

  def __repr__(self): return self.name

  def draw(self, num):
    round_events.append(f"{self} Draws {num} card(s)")
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
    round_events.append(f"{Self} received {amount}GP")
    self.gold += amount

  def pay_gold(self, amount, to_player=None):
    round_events.append(f"{self} pays {amount}GP")
    self.gold -= amount
    if to_player:
      round_events.append(f"{self.name} pays {amount} gold to {to_player}.")
      to_player.receive_gold(amount)

  def print_status(self, is_round_front_runner=False):
      if self == round_leader:
        name_display = f"{GRAY_BG}{self}{RESET}"
      elif is_round_front_runner:
        name_display = f"{BRIGHT_GREEN_BG}{self}{RESET}"
      else:
        name_display = f"{self}"
      # reformat flight for printing
      flight_reformatted = [value[0] for value in self.flight]
      print(f"{name_display}: {self.gold}GP, {self.hand_size} Cards")
      print(f"  Flight - {', '.join(flight_reformatted)}")

  def find_lowest_str(self):
    self.lowest_str_card = self.hand[0]
    for i in range(len(self.hand)):
      if self.hand[i][1] < self.lowest_str_card[1]:
        self.lowest_str_card = self.hand[i]
    return self.lowest_str_card

  def ante_card(self):
    #Ante lowest str card
    self.card_to_ante = self.find_lowest_str()
    self.hand.remove(self.card_to_ante)
    return [self, self.card_to_ante]
  
  def main_turn(self, last_str_played=None):
    # determine_strategy() function

    # plays strongest cards
    # Determine strongest
    strongest_card = self.hand[0]
    for card in self.hand:
      if card[1] > strongest_card[1]:
        strongest_card = card
    # Add to flight, remove from hand
    card_to_play = strongest_card
    self.flight.append(card_to_play)
    self.hand.remove(card_to_play)
    
    round_events.append(f"{self} plays {card_to_play[0]}")
    if last_str_played:
      if card_to_play[1] <= last_str_played:
        round_events.append(f"{self} POWER ACTIVATES")
    
    return card_to_play

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

def ante_phase():
  global stakes, round_leader, ante_pile, player_count
  
  acceptable_ante = False
  while not acceptable_ante:
    
    # Clear/Print for player ante
    clear()
    #print("--------------- PLAYER ANTE ---------------")

    # Retrieve Ante Cards
    returned_list = []
    for i in range(len(player_list)):
      # Returns [Player Class, [Card, STR]]
      returned_list.append(player_list[i].ante_card())
    
    clear()

    # Print ante results
    print("--------------- ANTE PHASE ---------------")
    # Print Player Antes
    for i in range(len(returned_list)):
      print(f"{returned_list[i][0]} antes: {returned_list[i][1][0]}")
    
    #time_to_sleep = 1 + (player_count / 2)
    #time.sleep(time_to_sleep)

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
    else: # Move on
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
        print("\n**All cards are tied with at least one other, so the first player will be chosen at random.**")
        first_player = random.choice(player_list)
    
  return first_player, highest_str_value

def proceed(clean_out=False):
  input("-->")
  if clean_out:
    # Move cursor up one line, then clear that line
    sys.stdout.write("\033[1A\033[2K")
    sys.stdout.flush()

def start_gambit():
  global round_leader, gambit_number, player_list, last_str_played, round_events, round_front_runner, ante_pile, discard_pile, stakes, current_round
  
  gambit_number += 1
  current_round = 0
  clear()
  print(f"START GAMBIT {gambit_number}")
  proceed()
  clear()
  
  # Clear Round Events
  round_events = []

  # Reset Stakes, Ante, and Flight
  stakes = 0
  if ante_pile:
    discard_pile = discard_pile + ante_pile
    ante_pile = []
  for player in player_list:
    if player.flight:
      discard_pile = discard_pile + player.flight
      player.flight = []

  # Players Draw 2 Cards
  if gambit_number > 1:
    for player in player_list:
      player.draw(2)

  # ANTE PHASE
  round_leader, ante_gold = ante_phase()
  print(f"\nEach player antes {ante_gold} gold.\n{round_leader} will start the round.")
  proceed()
  #clear()

  # THREE ROUNDS
  highest_card_so_far = None
  rounds = [1, 2, 3]
  for i in rounds:
    current_round += 1
    # Define Round Leader turn progression
    leader_index = player_list.index(round_leader)
    ordered_players = player_list[leader_index:] + player_list[:leader_index]
  
    # Round Variables
    last_str_played = [None]
    round_events = []
    cards_played_this_round = []

    # Each player takes a turn
    for player in ordered_players:
      # Return played card
      played_card = player.main_turn(last_str_played[-1])
      
      # update Last Strength played
      last_str_played.append(played_card[1])
      # Update cards played in round
      cards_played_this_round.append((player, played_card))
      
      # Recalculate Front runner after each play
      strength_values = [c[1] for _, c in cards_played_this_round]
      strength_counts = Counter(strength_values)
      untied_values = [v for v, count in strength_counts.items() if count == 1]
      # If at least one isn't tied
      if untied_values:
        # Find highest
        highest_untied = max(untied_values)
        # Find Player
        round_front_runner = next(p for p, c in cards_played_this_round if c[1] == highest_untied)
      else:
        # All are tied with at least one other
        round_front_runner = None

      # Print round events, having updated
      # the Flight and Front Runner color.
      # Wait for a PROCEED before running
      # next player's turn
     
      full_board(round_front_runner)
      proceed()
    

    # Round leader = Front_runner or the 
    # previous leader
    round_leader = round_front_runner if round_front_runner else round_leader

def full_board(front_runner=None):
  clear()
  
  # GAMBIT
  print(f"GAMBIT {gambit_number}")
  
  # TABLE VIEW
  print("--------------- TABLE VIEW ---------------")
  print(f"Stakes: {stakes}")
  reformatted_ante = [value[0] for value in ante_pile]
  print(f"Ante: {", ".join(reformatted_ante)}")
  for player in player_list:
    # pass through front_runner True/False
    lead_status = (player == front_runner)
    player.print_status(lead_status)
  
  # ROUND EVENTS
  print(f"--------------- ROUND {current_round} EVENTS --------------")
  if len(round_events) == 0:
    print("")
  else:
    for event in round_events:
      print(event)

# --------------------------------------
# --------------------------------------
# --------------------------------------    

# ---------- Number of Players ----------
player_count = None
while player_count not in ["2","3","4","5","6", ""]:
  player_count = input("How many players will there be? (2-6): ")
  # TESTING
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
  player_names_list.append(f"Player {num}")

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
last_str_played = None
rounds = [1, 2, 3]
winner = None
text_log = []
round_events = []
current_round = 0

# ---------- Start Game ----------
while not winner:
  start_gambit()


