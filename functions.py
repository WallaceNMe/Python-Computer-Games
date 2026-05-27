import random, sys, os
from gamestate import g
clear = lambda: os.system('clear')

# ----- FROM CLASSES -----

def find_lowest_str(player):
  lowest_str_card = player.hand[0]
  for i in range(len(player.hand)):
    if player.hand[i].strength < lowest_str_card.strength:
      lowest_str_card = player.hand[i]
  return lowest_str_card

def find_highest_str(player):
  highest_str_card = player.hand[0]
  for i in range(len(player.hand)):
    if player.hand[i].strength > highest_str_card.strength:
      highest_str_card = player.hand[i]
  return highest_str_card

# ----- Main -----

def check_stakes(g):
  if g.stakes == 0:
    return False

def shuffle_deck():
  random.shuffle(g.draw_pile)
  print("Deck was shuffled.")

def check_reshuffle():
  if len(g.draw_pile) == 0:
    # Copy adds insurance
    g.draw_pile = g.discard_pile.copy()
    g.discard_pile = []
    shuffle_deck()

def ante_phase():
  
  acceptable_ante = False
  while not acceptable_ante:
    
    # Retrieve Ante Cards
    returned_list = []
    for i in range(g.player_count):
      # Returns [Player, Card]
      returned_list.append(g.player_list[i].ante_card())

    # Print ANTE PHASE section
    clear()
    print("--------------- ANTE PHASE ---------------")
    for i in range(len(returned_list)):
      print(f"{returned_list[i][0]} antes: {returned_list[i][1]}")

    # ----- Check Ties -----

    # Collect strength values
    strength_values = [return_value[1].strength for return_value in returned_list]
    
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
        g.discard_pile.append(return_value[1])
        return_value[0].draw(1)
      proceed()
  
  # ----- Acceptable Ante -----

  # Add cards to ante_pile
  g.ante_pile = [return_value[1] for return_value in returned_list]

  # Pay to Stakes
  highest_str_value = max(strength_values)
  for player in g.player_list:
    player.pay_gold(highest_str_value)
    g.stakes += highest_str_value
  
  # ----- Determine First Player -----
  
  highest_untied = max(untied_values)
  first_player = [r[0] for r in returned_list if r[1].strength == highest_untied][0]
    
  return first_player, highest_str_value

def proceed(clean_out=False):
  input("-->")
  if clean_out:
    # Move cursor up one line, then clear that line
    sys.stdout.write("\033[1A\033[2K")
    sys.stdout.flush()

def gambit():
  g.gambit_number += 1
  g.current_round = 0
  clear()
  print(f"START GAMBIT {g.gambit_number}")
  proceed()
  clear()
  
  # Clear Round Events
  g.round_events = []

  # Reset Stakes, Ante, and Flight
  g.stakes = 0
  if g.ante_pile:
    g.discard_pile = g.discard_pile + g.ante_pile
    g.ante_pile = []
  for player in g.player_list:
    if player.flight:
      g.discard_pile = g.discard_pile + player.flight
      player.flight = []

  # Players Draw 2 Cards
  if g.gambit_number > 1:
    for player in g.player_list:
      player.draw(4)

  # ANTE PHASE
  g.round_leader, ante_gold = ante_phase()
  print(f"\nEach player antes {ante_gold} gold.\n{g.round_leader} will start the round.")
  proceed()

  # ---------- THREE ROUNDS ----------

  highest_card_so_far = None
  g.rounds = [1, 2, 3]
  for i in g.rounds:
    g.current_round += 1
    # Define Round Leader turn progression
    leader_index = g.player_list.index(g.round_leader)
    ordered_players = g.player_list[leader_index:] + g.player_list[:leader_index]
  
    # Round Variables
    last_str_played = [None]
    g.round_events = []
    cards_played_this_round = []

    # Each player takes a turn
    for player in ordered_players:
      # Buy Cards
      if len(player.hand) <= 1:
        check_buy_cards(player)
      
      #Check hand max
      player.check_hand_max()

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
        g.round_front_runner = next(p for p, c in cards_played_this_round if c[1] == highest_untied)
      else:
        # All are tied with at least one other
        g.round_front_runner = None

      # Print round events, having updated
      # the Flight and Front Runner color.
      # Wait for a PROCEED before running
      # next player's turn
     
      full_board(g.round_front_runner)
      proceed(True)

      if player == ordered_players[-1]:
        if g.round_front_runner and i != g.rounds[-1]:
          print(f"End Round. {g.round_front_runner} will start the next round.")
        elif not g.round_front_runner and i != g.rounds[-1]:
          print(f"End Round. {g.round_leader} will start the next round.")
        else:
          print("End Round.")

        proceed()
    

    # Round leader = Front_runner or the previous leader
    g.round_leader = g.round_front_runner if g.round_front_runner else g.round_leader

    # ---------- DETERMINE WINNER ----------
    if i == g.rounds[-1]:
      determine_gambit_winner()

    # ---------- CHECK END GAME ----------
    for player in g.player_list:
      if player.gold <= 0:
        g.loser = player
 
def full_board(front_runner=None):
  clear()
  
  # GAMBIT
  print(f"GAMBIT {g.gambit_number}")
  
  # TABLE VIEW
  print("--------------- TABLE VIEW ---------------")
  print(f"Stakes: {g.stakes}")
  reformatted_ante = [value[0] for value in g.ante_pile]
  print(f"Ante: {", ".join(reformatted_ante)}")
  for player in g.player_list:
    # pass through front_runner True/False
    lead_status = (player == front_runner)
    player.print_status(lead_status)
  
  # ROUND EVENTS
  print(f"--------------- ROUND {g.current_round} EVENTS --------------")
  if len(g.round_events) == 0:
    print("")
  else:
    for event in g.round_events:
      print(event)

def check_special_flights(player):
  # Strength = steal that much gold from the stakes and take two ante cards.
  strengths = [card[1] for card in player.flight]
  strength_counts = Counter(strengths)
  has_strength_flight = any(count >= 3 for count in strength_counts.values())
  if has_strength_flight:
    value = None
    for strength, count in strength_counts.items():
      if count == 3:
        value = strength
        break
    gold_taken = min(value, g.stakes)
    g.stakes -= gold_taken
    player.receive_gold(gold_taken)
    # STEAL ANTE CARDS
    if player == g.player_list[0]:
      print(f"You have completed a Strength Flight! Each player pays you {gold_taken}GP, and you may select up to 2 ante cards to add to your hand.")
      if g.ante_pile: 
        taken = 0
        while g.ante_pile and taken < 2:
          for i, card in enumerate(g.ante_pile, 1):
            print(f"  {i}. {card[0]}")
          acceptable_input = False
          while not acceptable_input:
            choice = input(f"Card Choice {taken + 1}: ")
            try:
              choice = int(choice)
              if choice in range(1,len(g.draw_pile)+1):
                chosen_card = g.ante_pile[choice - 1]
                acceptable_input = True
            except ValueError:
              print("Enter a valid number.")
          g.ante_pile.remove(chosen_card)
          player.hand.append(chosen_card)
          taken += 1
    else:
      g.round_events.append(f"{player} has completed a Strength Flight! Each player pays {player} {gold_taken}GP, and {player} may 2 ante cards.")
      for person in g.player_list:
        if person != player:
          player.pay_gold(value, player)
      taken = 0
      while g.ante_pile and taken < 0:
        card = g.ante_pile.pop()
        player.hand.append(card)


  # Color = each opponent pays gold to you equal to your second strongest dragon
  color_counts = Counter()
  for card in player.flight:
    for color in card[4]:
      color_counts[color] += 1  
  has_color_flight = any(count >= 3 for count in color_counts.values())
  if has_color_flight:
    second_strongest = None
    for color, count in color_counts.items():
      if count == 3:
        color_cards = [card for card in player.flight if color in card[4]]
        colored_cards.sort(key=lambda card: card[1], reverse=True)
        second_strongest = color_cards[1][1]
        break
    player_index = g.player_list.index(player)
    players_to_be_stealt_from = g.player_list[:player_index] + g.player_list[player_index + 1:]
    for person in players_to_be_stealt_from:
      person.pay_gold(second_strongest, player)
    g.round_events.append(f"{player} has completed a Color Flight! Each player pays {player} {second_strongest}GP.")

def determine_gambit_winner():

  while True:
    # TOtal flights, find max, check ties
    flight_totals = {player: sum(card[1] for card in player.flight) for player in g.player_list}
    max_total = max(flight_totals.values())
    tied_players = [p for p, total in flight_totals.items() if total == max_total]

    # Print Board and results
    full_board()
    print("--------------- END GAMBIT ---------------")
    for player in g.player_list:
      print(f"{player.name}: Flight Total = {flight_totals[player]}")

    # No Ties
    if len(tied_players) == 1:
      gambit_winner = tied_players[0]
      gambit_winner.receive_gold(g.stakes)
      g.stakes = 0
      print(f"\n{gambit_winner} wins the gambit and collects the pot!")
      
      # Check debt
      for player in g.player_list:
        if player.debt:
          if player.debt >= player.gold:
            g.loser = player
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
      print(f"\n{g.YELLOW_BG}TIE between: {tied_names} — tiebreaker round!{g.RESET}")
      proceed()

      g.current_round += 1
      g.round_events = []
      last_str_played = [None]

      # Determine order by round_leader or clockwise
      if g.round_leader in tied_players:
        leader_index = tied_players.index(g.round_leader)
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

def print_traditional():
  clear()
  for card in g.traditional_mortals_list:
    color = g.MAGENTA_BG if card.type == 'Mortal' else g.YELLOW_BG
    aditional_reformatted = [f"{g.GRAY_BG}{card} [{card.alignment}]{g.RESET} - {card.power}" for card in g.traditional_mortals_list]
  counter = 1
  for item in traditional_reformatted:
    print(f"{counter}.) {item}")
    counter += 1
  proceed()

def print_special_card_options():
  print("How would you like to include special cards?")
  print("  1. Pick 'em  - Each player chooses 1 special card. The rest are chosen randomly.")
  print("  2. Show 'em  - 10 cards are chosen randomly and revealed to all players.")
  print("  3. Among Friends - 10 cards are chosen randomly without revealing them.")
  print("  4. Traditional ('v' to view)")

def ten_random():
  options = g.mortals_list + g.special_dragons_list
  chosen = random.sample(options, 10)
  return chosen

def print_random_ten(full=False):
  print("Special Cards: ('v' to view)")
  counter = 1
  for card in g.picked_cards:
    is_mortal = True if card in g.mortals_list else False
    if is_mortal:
      color = g.MAGENTA_BG
    else:
      color = g.BRIGHT_YELLOW_BG
    if full:
      final_half = f" - {card.power}"
    else:
      final_half = ""
    print(f"  {counter}.) {color}{card}{g.RESET}{final_half}")
    counter += 1
  response = input("-->")
  if response.upper() == 'V':
    print_random_ten(True)
