import random
from gamestate import g
from functions import check_reshuffle, find_lowest_str, find_highest_str, clear, full_board

class User():
  def __init__(self, name):
    self.name = name
    self.hand = []
    self.gold = g.starting_gold
    self.flight = []
    self.debt = 0

  def __repr__(self): 
    return self.name
  
  def receive_gold(self, amount):
    self.gold += amount

  def pay_gold(self, amount, to_player=None):
    # If you can pay
    if self.gold >= amount:
        self.gold -= amount
        # Pay to a player
        if to_player:
            to_player.receive_gold(amount)
            g.round_events.append(f"{self} pays {amount} gold to {to_player}")
        else:
          # Basic Payment
          g.round_events.append(f"{self} pays {amount} gold")
    else:
        # Pay what you can, track the rest as debt
        shortfall = amount - self.gold
        actually_paid = self.gold
        self.gold = 0
        self.debt += shortfall
        if to_player:
            to_player.receive_gold(actually_paid)
            g.round_events.append(f"{self} pays {actually_paid} gold to {to_player}")
        else:
          g.round_events.append(f"{self} pays {actually_paid} gold")
        g.round_events.append(f"{self} has exhausted their hoard.")

  def draw(self, num):
    if num == 1:
      g.round_events.append(f"{self} draws {num} card")
      new_card = g.draw_pile.pop()
      self.hand.append(new_card)
      check_reshuffle()
      g.round_events.append(f"You have drawn: {new_card}")
    elif num > 1:
      g.round_events.append(f"{self} draws {num} cards")
      drawn_cards = []
      for i in range(num):
        new_card = g.draw_pile.pop()
        check_reshuffle()
        drawn_cards.append(new_card)
        self.hand.append(new_card)
      drawn_cards = [card.name for card in drawn_cards]
      g.round_events.append(f"You have drawn: {', '.join(drawn_cards)}")         

  def check_buy_cards(self):
    if len(self.hand) == 1:
      g.round_events.append("You only have 1 card left in hand, and must buy cards.")
      self.buy_cards()
    elif len(self.hand) == 0:
      reound_events.append("You have no cards left in hand and must immediately buy cards.")
      self.buy_cards()

  def buy_cards(self):
    price_card = g.draw_pile.pop()
    payment = price_card.strength
    difference = 4 - len(self.hand)
    g.round_events.append(f"{self} has drawn: {price_card} and will pay {payment}GP to buy {difference} cards.")

    self.pay_gold(payment)
    g.stakes += payment
    self.draw(difference)

  def check_hand_max(self):
    if len(self.hand) > 10:
      num = len(self.hand) - 10
      g.round_events.append(f"{self} has exceeded the hand maximum and must discard {num} card(s)")
      removing = []
      for i in range(num):
        to_discard = self.choose_card("DISCARD")
        removing.append(to_discard)
        self.hand.remove(to_discard)
      removing_reformatted = ', '.join(removing)
      g.round_events.append(f"{self} discards {removing_reformatted}")

  def choose_card(self, header, last_str_played=None):

    # Acceptable Inputs
    acceptable_inputs = list(range(1, len(self.hand) + 1))
    additional = ["", "sc", "s", "sh"]
    acceptable_inputs = acceptable_inputs + additional

    # Reprints for sorting commands
    reprint_necessary = True
    while reprint_necessary:
      # Full print
      full_board()
      
      # Header
      print(f"--------------- {header} ---------------")
      
      # Print previous STR (Gray)
      if last_str_played:
        print(f"{g.GRAY_BG}Last card was STR {last_str_played}{g.RESET}")
      # List Cards
      print("YOUR HAND:")
      for i, card in enumerate(self.hand, 1):
        print(f"  {i}. {card}")
      # Commands
      print("CMD: s, sc, sh")
      
      returned_input = None
      while returned_input not in acceptable_inputs:
        chosen_card = None
        returned_input = input(f"Choose a card (1-{len(self.hand)}): ")
        try:
          # If acceptable integer: card chosen
          returned_input = int(returned_input)
          if returned_input in acceptable_inputs:
            chosen_card = self.hand[returned_input - 1]
            reprint_necessary = False
          else:
            print(f"Please enter a number between 1 and {len(self.hand)}.")
            returned_input = None
        except ValueError:
          # If NOT a number
          if returned_input in acceptable_inputs:
            # ENTER
            if returned_input == "":
              if is_ante:
                chosen_card = find_lowest_str(self)
              elif current_turn:
                chosen_card = find_highest_str(self)
              reprint_necessary = False
            # S
            elif returned_input == "s":
              self.hand.sort(key=lambda card: card.strength, reverse = True)
              reprint_necessary = True
              break
            # SC
            elif returned_input == "sc":
              self.hand.sort(key=lambda card: card.name)
              #self.hand.sort(key=lambda card: card.split()[0])
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

  def print_status(self, is_front_runner=False):
    if self == g.round_leader:
      # Previous Leader
      name_display = f"{GRAY_BG}{self}{RESET}"
    elif is_front_runner:
      # Favored Leader
      name_display = f"{BRIGHT_GREEN_BG}{self}{RESET}"
    else:
      # Regular
      name_display = f"{self}"
    
    # reformat flight for printing
    #flight_reformatted = [card for card in player.flight]
    
    #Debt
    gold_or_debt = None
    if self.gold:
      gold_or_debt = f"{self.gold}GP"
    else:
      gold_or_debt = f"{RED_BG}{self.debt}GP DEBT{RESET}"

    print(f"{name_display}: {gold_or_debt}, {len(self.hand)} Cards")
    print(f"  Flight - {', '.join(self.flight)}")

  def ante_card(self):
    ante_card = self.choose_card("ANTE PHASE")
    self.hand.remove(ante_card)
    return [self, ante_card]
  
  def main_turn(self,last_str_played):
    # Choose Card
    card = self.choose_card("PLAYER TURN", last_str_played)
    g.round_events.append(f"{self} Plays {card[0]}")

    # Power Activates?
    if last_str_played:
      if card.strength <= last_str_played:
        power_activates = True
        g.round_events.append(f"{self} POWER ACTIVATES")
      else:
        power_activates = False
    else:
      power_activates = True
      g.round_events.append(f"{self} POWER ACTIVATES")
    
    self.flight.append(card)
    self.hand.remove(card)
    return card

class Player():

  def __init__(self, name):
    self.name = name
    self.hand = []
    self.gold = g.starting_gold
    self.flight = []
    self.debt = 0

  def __repr__(self): 
    return self.name
  
  def receive_gold(self, amount): 
    self.gold += amount

  def draw(self, num):
    if num == 1:
      g.round_events.append(f"{self} draws {num} card")
    elif num > 1:
      g.round_events.append(f"{self} draws {num} cards")
    for i in range(num):
      new_card = g.draw_pile.pop()
      self.hand.append(new_card)
      check_reshuffle()

  def buy_cards(self):
    price_card = g.draw_pile.pop()
    payment = price_card.strength
    difference = 4 - len(self.hand)
    g.round_events.append(f"{self} has drawn: {price_card} and will pay {payment}GP to buy {difference} cards.")

    self.pay_gold(payment)
    g.stakes += payment
    self.draw(difference)

  def check_hand_max(self):
    # MUST BE CHANGED WHEN PLAYER STRATEGY FUNCTION IN PLACE
    if len(self.hand) > 10:
      num = len(self.hand) - 10
      g.round_events.append(f"{self} has exceeded the hand maximum and must discard {num} card(s)")
      removing = []
      for i in range(num):
        to_discard = self.choose_card("DISCARD")
        removing.append(to_discard)
        self.hand.remove(to_discard)
      removing_reformatted = ', '.join(removing)
      g.round_events.append(f"{self} discards {removing_reformatted}")

  def pay_gold(self, amount, to_player=None):
    if self.gold >= amount:
        self.gold -= amount
        if to_player:
            to_player.receive_gold(amount)
            g.round_events.append(f"{self} pays {amount} gold to {to_player}")
        else:
          g.round_events.append(f"{self} pays {amount} gold")
    else:
        # Pay what you can, track the rest as debt
        shortfall = amount - self.gold
        actually_paid = self.gold
        self.gold = 0
        self.debt += shortfall
        if to_player:
            to_player.receive_gold(actually_paid)
            g.round_events.append(f"{self} pays {actually_paid} gold to {to_player}")
        else:
          g.round_events.append(f"{self} pays {actually_paid} gold")
        g.round_events.append(f"{self} has exhausted their hoard.")

  def check_buy_cards(self):
    if len(self.hand) == 1:
      g.round_events.append(f"{self} only has 1 card left in hand, and must buy cards.")
      self.buy_cards()
    elif len(self.hand) == 0:
      round_events.append(f"{self} has no cards left in hand and must immediately buy cards.")
      self.buy_cards()

  def print_status(self, is_front_runner=False):
    if self == g.round_leader:
      # Previous Leader
      name_display = f"{GRAY_BG}{self}{RESET}"
    elif is_front_runner:
      # Favored Leader
      name_display = f"{BRIGHT_GREEN_BG}{self}{RESET}"
    else:
      # Regular
      name_display = f"{self}"
    
    # reformat flight for printing
    #flight_reformatted = [card for card in player.flight]
    
    #Debt
    gold_or_debt = None
    if self.gold:
      gold_or_debt = f"{self.gold}GP"
    else:
      gold_or_debt = f"{RED_BG}{self.debt}GP DEBT{RESET}"

    print(f"{name_display}: {gold_or_debt}, {len(self.hand)} Cards")
    print(f"  Flight - {', '.join(self.flight)}")

  def ante_card(self):
    #Ante lowest str card
    self.card_to_ante = find_lowest_str(self)
    self.hand.remove(self.card_to_ante)
    return [self, self.card_to_ante]
  
  def main_turn(self, last_str_played=None):
    # determine_strategy() function
    # Add to flight, remove from hand
    card_to_play = find_highest_str(self)
    self.flight.append(card_to_play)
    self.hand.remove(card_to_play)
    
    g.round_events.append(f"{self} plays {card_to_play[0]}")

    if last_str_played:
      if card_to_play.strength <= last_str_played:
        power_activates = True
        g.round_events.append(f"{self} POWER ACTIVATES")
      else:
        power_activates = False
    else:
      power_activates = True
      g.round_events.append(f"{self} POWER ACTIVATES")
    
    return card_to_play
