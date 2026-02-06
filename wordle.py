import random, os, time
clear = lambda: os.system('cls' if os.name == 'nt' else 'clear') 

GREEN_BG = '\033[42m\033[30m\033[1m'
YELLOW_BG = '\033[43m\033[30m\033[1m'
GRAY_BG = '\033[100m\033[37m\033[1m'
RESET = '\033[0m'

word_list = ["PURSE", "HORSE", "CLUES", "GOOSE"]
secret_word = random.choice(word_list)

# Player guesses
guess_one = [" ", " ", " ", " ", " "]
guess_two = [" ", " ", " ", " ", " "]
guess_three = [" ", " ", " ", " ", " "]
guess_four = [" ", " ", " ", " ", " "]
guess_five = [" ", " ", " ", " ", " "]

# ----- FUNCTIONS -----

def print_board():
  global guess_one, guess_two, guess_three, guess_four, guess_five

  clear()
  print(f"|{guess_one[0]}|{guess_one[1]}|{guess_one[2]}|{guess_one[3]}|{guess_one[4]}|")
  print(f"|{guess_two[0]}|{guess_two[1]}|{guess_two[2]}|{guess_two[3]}|{guess_two[4]}|")
  print(f"|{guess_three[0]}|{guess_three[1]}|{guess_three[2]}|{guess_three[3]}|{guess_three[4]}|")
  print(f"|{guess_four[0]}|{guess_four[1]}|{guess_four[2]}|{guess_four[3]}|{guess_four[4]}|")
  print(f"|{guess_five[0]}|{guess_five[1]}|{guess_five[2]}|{guess_five[3]}|{guess_five[4]}|")

def check(current_guess):
  global secret_word, answered

  current_guess_colored_letters = []
  for i in range(len(current_guess)):
    if current_guess[i] in secret_word:
      if current_guess[i] == secret_word[i]:
        current_guess_colored_letters.append(GREEN_BG + current_guess[i] + GREEN_BG + RESET)
      else:
        current_guess_colored_letters.append(YELLOW_BG + current_guess[i] + YELLOW_BG + RESET)
    else:
      current_guess_colored_letters.append(GRAY_BG + current_guess[i] + GRAY_BG + RESET)

  return current_guess_colored_letters

# ----- GUESS FUNCTIONS -----

def turn_five():
  global guess_five, secret_word

  five = ""
  while len(five) != 5:
    print_board()
    five = input("Guess five: ").upper()

  saved_guess_five = five
  guess_five = check(five)
  print_board()

  # Check win
  if saved_guess_five == secret_word:
    print("Finally! I thought you'd never guess it.")
  else:
    print("Looks like you looooooooooooz!")
    time.sleep(2)
    print(f"The word was {secret_word}")

def turn_four():
  global guess_four

  four = ""
  while len(four) != 5:
    print_board()
    four = input("Guess four: ").upper()

  saved_guess_four = four
  guess_four = check(four)
  print_board()

  # Check win
  if saved_guess_four == secret_word:
    print("Not bad.")
  else:
    print("Clock's ticking")
    time.sleep(1)
    print("tick tick tick ...")
    time.sleep(1)
    turn_five()

def turn_three():
  global guess_three

  three = ""
  while len(three) != 5:
    print_board()
    three = input("Guess three: ").upper()

  saved_guess_three = three
  guess_three = check(three)
  print_board()

  # Check win
  if saved_guess_three == secret_word:
    print("Not bad.")
  else:
    turn_four()

def turn_two():
  global guess_two

  two = ""
  while len(two) != 5:
    print_board()
    two = input("Guess two: ").upper()

  saved_guess_two = two
  guess_two = check(two)
  print_board()

  # Check win
  if saved_guess_two == secret_word:
    print("\nWow. So Impressed.")
  else:
    turn_three()

def turn_one():
  global guess_one
  
  print_board()

  one = ""
  while len(one) != 5:
    print_board()
    one = input("Guess one: ").upper()  

  saved_guess_one = one
  guess_one = check(one)
  print_board()

  # Check win
  if saved_guess_one == secret_word:
    print("\nCheater.")
  else:
    turn_two()

# ----- START GAME -----

turn_one()
