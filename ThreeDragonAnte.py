import random, time, os, sys
from variables import name_list, deck_list, traditional_mortals_list
from collections import Counter
clear = lambda: os.system('clear')

# Changed card format. Fix errors.
# Review player.debt tracking system
# player.buy_cards() - Immediately if no cards, or at start of turn if only 1
# Special Flights
# Hand max of 10
# Power activates for Legendary Dragons

# Later
# -----
# No gold in stakes: gambit ends immediately
# Players cannot steal negative into the stakes
# Remove enter for player choice auto select
# Remove draw 3 cards feature in gambit.

# Check all places where draw_pile.pop() is called. Make sure there is a check_reshuffle() after it. 
# Compile a README or game manual that prints at the start of the game. Include choose card commands
# Draw() prints "You have drawn X". Is that ok for round events/progression.
# Computers that will steal cards will take the last or first card in the player's hand to try and get a high card. Players can shuffle their hands before choosing which card to give up to avoid this. 

GREEN_BG = '\033[42m\033[30m\033[1m'
YELLOW_BG = '\033[43m\033[30m\033[1m'
GRAY_BG = '\033[100m\033[37m\033[1m'
RESET = '\033[0m'
RED_BG = '\033[41m\033[30m\033[1m'
BLUE_BG = '\033[44m\033[30m\033[1m'
MAGENTA_BG = '\033[45m\033[30m\033[1m'
CYAN_BG = '\033[46m\033[30m\033[1m'
WHITE_BG = '\033[47m\033[30m\033[1m'
BRIGHT_RED_BG = '\033[101m\033[30m\033[1m'
BRIGHT_GREEN_BG = '\033[102m\033[30m\033[1m'
BRIGHT_YELLOW_BG = '\033[103m\033[30m\033[1m'
BRIGHT_BLUE_BG = '\033[104m\033[30m\033[1m'
BRIGHT_MAGENTA_BG = '\033[105m\033[30m\033[1m'
BRIGHT_CYAN_BG = '\033[106m\033[30m\033[1m'
BRIGHT_WHITE_BG = '\033[107m\033[30m\033[1m'
BLUE_BG_WHITE = '\033[44m\033[37m\033[1m'
RED_BG_WHITE = '\033[41m\033[37m\033[1m'
MAGENTA_BG_WHITE = '\033[45m\033[37m\033[1m'

# Card format: ["Green 7", 7, "Evil", "Card effect"]

# Select Mortals
mortals_list = traditional_mortals_list

# Add Mortals to dragons
for card in mortals_list:
  deck_list.append(card)

# Card Lists
draw_pile = deck_list.copy()
discard_pile = []
ante_pile = []

# --------------------------------------
# --------------- CLASSES --------------
# --------------------------------------

class User():
  def __init__(self, player_id, name, hand, starting_gold):
    self.id = player_id
    self.name = name
    self.hand = hand
    self.gold = starting_gold
    self.hand_size = len(self.hand)
    self.flight = []
    self.debt = 0

  def __repr__(self): return self.name
  def receive_gold(self, amount): self.gold += amount

  def pay_gold(self, amount, to_player=None):
    if self.gold >= amount:
        self.gold -= amount
        if to_player:
            to_player.receive_gold(amount)
            round_events.append(f"{self} pays {amount} gold to {to_player}")
        else:
          round_events.append(f"{self} pays {amount} gold")
    else:
        # Pay what you can, track the rest as debt
        shortfall = amount - self.gold
        actually_paid = self.gold
        self.gold = 0
        self.debt += shortfall
        if to_player:
            to_player.receive_gold(actually_paid)
            round_events.append(f"{self} pays {actually_paid} gold to {to_player}")
        else:
          round_events.append(f"{self} pays {actually_paid} gold")
        round_events.append(f"{self} has exhausted their hoard.")

  def find_lowest_str(self):
    lowest_str_card = self.hand[0]
    for i in range(len(self.hand)):
      if self.hand[i][1] < lowest_str_card[1]:
        lowest_str_card = self.hand[i]
    return lowest_str_card

  def find_highest_str(self):
    highest_str_card = self.hand[0]
    for i in range(len(self.hand)):
      if self.hand[i][1] > highest_str_card[1]:
        highest_str_card = self.hand[i]
    return highest_str_card

  def draw(self, num):
    if num == 1:
      round_events.append(f"{self} draws {num} card")
      new_card = draw_pile.pop()
      self.hand.append(new_card)
      check_reshuffle()
      round_events.append(f"You have drawn: {new_card[0]}")
    elif num > 1:
      round_events.append(f"{self} draws {num} cards")
      drawn_cards = []
      for i in range(num):
        new_card = draw_pile.pop()
        check_reshuffle()
        drawn_cards.append(new_card)
        self.hand.append(new_card)
      drawn_reformatted = [value[0] for value in drawn_cards]
      round_events.append(f"You have drawn: {', '.join(drawn_reformatted)}")
          

  def buy_cards(self):
    if self.hand_size == 1:
      round_events.append(f"{self} only has 1 card left in hand, and must buy cards.")
    elif self.hand_size == 0:
      reound_events.append(f"{self} has no cards left in hand and must immediately buy cards.")
    
    price_card = draw_pile.pop()
    payment = price_card[1]
    difference = 4 - self.hand_size
    round_events.append(f"{self} has drawn: {price_card} and will pay {payment}GP to buy {difference} cards.")

    self.pay_gold(payment)
    stakes += payment
    self.draw(difference)

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
      
      #Debt
      gold_or_debt = None
      if self.gold:
        gold_or_debt = f"{self.gold}GP"
      else:
        gold_or_debt = f"{RED_BG}{self.debt}GP DEBT{RESET}"

      print(f"{name_display}: {gold_or_debt}, {self.hand_size} Cards")
      print(f"  Flight - {', '.join(flight_reformatted)}")

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
        print(f"{GRAY_BG}Last card was STR {last_str_played}{RESET}")
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
              if is_ante:
                chosen_card = self.find_lowest_str()
              elif current_turn:
                chosen_card = self.find_highest_str()
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
  
  def main_turn(self,last_str_played):
    # Choose Card
    card = self.choose_card(False, True, last_str_played)
    round_events.append(f"{self} Plays {card[0]}")

    # Power Activates?
    if last_str_played:
      if card[1] <= last_str_played:
        power_activates = True
        round_events.append(f"{self} POWER ACTIVATES")
      else:
        power_activates = False
    else:
      power_activates = True
      round_events.append(f"{self} POWER ACTIVATES")
    
    self.flight.append(card)
    self.hand.remove(card)
    return card

class Player():

  def __init__(self, player_id, name, hand, starting_gold):
    self.id = player_id
    self.name = name
    self.hand = hand
    self.gold = starting_gold
    self.hand_size = len(self.hand)
    self.flight = []
    self.debt = 0

  def __repr__(self): return self.name
  def receive_gold(self, amount): self.gold += amount

  def draw(self, num):
    if num == 1:
      round_events.append(f"{self} draws {num} card")
    elif num > 1:
      round_events.append(f"{self} draws {num} cards")
    for i in range(num):
      new_card = draw_pile.pop()
      self.hand.append(new_card)
      check_reshuffle()

  def buy_cards(self):
    if self.hand_size == 1:
      round_events.append(f"{self} only has 1 card left in hand, and must buy cards.")
    elif self.hand_size == 0:
      reound_events.append(f"{self} has no cards left in hand and must immediately buy cards.")
    
    price_card = draw_pile.pop()
    payment = price_card[1]
    difference = 4 - self.hand_size
    round_events.append(f"{self} has drawn: {price_card} and will pay {payment}GP to buy {difference} cards.")

    self.pay_gold(payment)
    stakes += payment
    self.draw(difference)

  def pay_gold(self, amount, to_player=None):
    if self.gold >= amount:
        self.gold -= amount
        if to_player:
            to_player.receive_gold(amount)
            round_events.append(f"{self} pays {amount} gold to {to_player}")
        else:
          round_events.append(f"{self} pays {amount} gold")
    else:
        # Pay what you can, track the rest as debt
        shortfall = amount - self.gold
        actually_paid = self.gold
        self.gold = 0
        self.debt += shortfall
        if to_player:
            to_player.receive_gold(actually_paid)
            round_events.append(f"{self} pays {actually_paid} gold to {to_player}")
        else:
          round_events.append(f"{self} pays {actually_paid} gold")
        round_events.append(f"{self} has exhausted their hoard.")

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
      #Debt
      gold_or_debt = None
      if self.gold:
        gold_or_debt = f"{self.gold}GP"
      else:
        gold_or_debt = f"{RED_BG}{self.debt}GP DEBT{RESET}"
      print(f"{name_display}: {gold_or_debt}, {self.hand_size} Cards")
      print(f"  Flight - {', '.join(flight_reformatted)}")

  def find_lowest_str(self):
    lowest_str_card = self.hand[0]
    for i in range(len(self.hand)):
      if self.hand[i][1] < lowest_str_card[1]:
        lowest_str_card = self.hand[i]
    return lowest_str_card

  def find_highest_str(self):
    strongest_card = self.hand[0]
    for card in self.hand:
      if card[1] > strongest_card[1]:
        strongest_card = card
    return strongest_card

  def ante_card(self):
    #Ante lowest str card
    self.card_to_ante = self.find_lowest_str()
    self.hand.remove(self.card_to_ante)
    return [self, self.card_to_ante]
  
  def main_turn(self, last_str_played=None):
    # determine_strategy() function
    # Add to flight, remove from hand
    card_to_play = self.find_highest_str()
    self.flight.append(card_to_play)
    self.hand.remove(card_to_play)
    
    round_events.append(f"{self} plays {card_to_play[0]}")

    if last_str_played:
      if card_to_play[1] <= last_str_played:
        power_activates = True
        round_events.append(f"{self} POWER ACTIVATES")
      else:
        power_activates = False
    else:
      power_activates = True
      round_events.append(f"{self} POWER ACTIVATES")
    
    return card_to_play

# -------------------------------------
# ------------- FUNCTIONS -------------
# -------------------------------------

def check_stakes():
  if stakes == 0:
    return False

def shuffle_deck():
  random.shuffle(draw_pile)
  print("Deck was shuffled.")

def check_reshuffle():
  global draw_pile, discard_pile
  if len(draw_pile) == 0:
    # Copy adds insurance
    draw_pile = discard_pile.copy()
    discard_pile = []
    shuffle_deck()

def ante_phase():
  global stakes, round_leader, ante_pile, player_count, round_events
  
  acceptable_ante = False
  while not acceptable_ante:
    
    # Retrieve Ante Cards
    returned_list = []
    for i in range(len(player_list)):
      # Returns [Player, [Card, STR]]
      returned_list.append(player_list[i].ante_card())

    # Print ANTE PHASE section
    clear()
    print("--------------- ANTE PHASE ---------------")
    for i in range(len(returned_list)):
      print(f"{returned_list[i][0]} antes: {returned_list[i][1][0]}")

    # ----- Check Ties -----

    # Collect strength values
    strength_values = [return_value[1][1] for return_value in returned_list]
    
    # Count occurrences of each strength value
    strength_counts = Counter(strength_values)
    
    # Collect untied values
    untied_values = [value for value, count in strength_counts.items() if count == 1]

    # At least 1 untied value = acceptable ante
    if untied_values:
      acceptable_ante = True
    else:
      print("\nAll ante cards were tied with at least one other card. Each player draws a card and re-antes.\n")

      # Discard / Draw for each player
      for return_value in returned_list:
        discard_pile.append(return_value[1])
        return_value[0].draw(1)
      proceed()
  
  # ----- Acceptable Ante -----

  # Add cards to ante_pile
  ante_pile = [return_value[1] for return_value in returned_list]

  # Pay to Stakes
  highest_str_value = max(strength_values)
  for player in player_list:
    player.pay_gold(highest_str_value)
    stakes += highest_str_value
  
  # ----- Determine First Player -----
  
  highest_untied = max(untied_values)
  first_player = [r[0] for r in returned_list if r[1][1] == highest_untied][0]
    
  return first_player, highest_str_value

def proceed(clean_out=False):
  input("-->")
  if clean_out:
    # Move cursor up one line, then clear that line
    sys.stdout.write("\033[1A\033[2K")
    sys.stdout.flush()

def gambit():
  global round_leader, gambit_number, player_list, last_str_played, round_events, round_front_runner, ante_pile, discard_pile, stakes, current_round, loser
  
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
      player.draw(4)

  # ANTE PHASE
  round_leader, ante_gold = ante_phase()
  print(f"\nEach player antes {ante_gold} gold.\n{round_leader} will start the round.")
  proceed()
  #clear()

  # ---------- THREE ROUNDS ----------

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
      # Buy Cards
      if player.hand_size <= 1:
        player.buy_cards()

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
      proceed(True)

      if player == ordered_players[-1]:
        if round_front_runner and i != rounds[-1]:
          print(f"End Round. {round_front_runner} will start the next round.")
        elif not round_front_runner and i != rounds[-1]:
          print(f"End Round. {round_leader} will start the next round.")
        else:
          print("End Round.")

        proceed()
    

    # Round leader = Front_runner or the previous leader
    round_leader = round_front_runner if round_front_runner else round_leader

    # ---------- DETERMINE WINNER ----------
    if i == rounds[-1]:
      determine_gambit_winner()

    # ---------- CHECK END GAME ----------
    for player in player_list:
      if player.gold <= 0:
        loser = player
 
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

def check_special_flights():
  # Color = each opponent pays gold to you equal to your second strongest dragon
  # Strength = steal that much gold from the stakes and take two ante cards.
  global stakes
  

def determine_gambit_winner():
  global stakes, round_leader, current_round, round_events

  while True:
    # TOtal flights, find max, check ties
    flight_totals = {player: sum(card[1] for card in player.flight) for player in player_list}
    max_total = max(flight_totals.values())
    tied_players = [p for p, total in flight_totals.items() if total == max_total]

    # Print Board and results
    full_board()
    print("--------------- END GAMBIT ---------------")
    for player in player_list:
      print(f"{player.name}: Flight Total = {flight_totals[player]}")

    # No Ties
    if len(tied_players) == 1:
      gambit_winner = tied_players[0]
      gambit_winner.receive_gold(stakes)
      stakes = 0
      print(f"\n{gambit_winner} wins the gambit and collects the pot!")
      
      # Check debt
      for player in player_list:
        if player.debt:
          if player.debt >= player.gold:
            loser = player
          else:
            # Pay debt to the house
            player.pay_gold(player.debt)
            print(f"{player} pays {player.debt} gold to the House.")

      proceed()
      return

    # Ties
    else:
      # Tiebreaker: tied players each play one more card
      tied_names = ", ".join(str(p) for p in tied_players)
      print(f"\n{YELLOW_BG}TIE between: {tied_names} — tiebreaker round!{RESET}")
      proceed()

      current_round += 1
      round_events = []
      last_str_played = [None]

      # Determine order by round_leader or clockwise
      if round_leader in tied_players:
        leader_index = tied_players.index(round_leader)
        ordered_tied = tied_players[leader_index:] + tied_players[:leader_index]
      else:
        ordered_tied = tied_players

      # Player turns
      for player in ordered_tied:
        #if not player.hand:
          #player.draw(1)
        played_card = player.main_turn(last_str_played[-1])
        last_str_played.append(played_card[1])
        full_board()
        proceed()

      # Loop back up to re-evaluate flight totals

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
loser = False
round_front_runner = None

# ---------- Start Game ----------
while not loser:
  gambit()

clear()
print(f"{loser} has no more gold. Thank you for playing.")

