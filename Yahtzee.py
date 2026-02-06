import random, sys, os
clear = lambda: os.system('clear')

#SPOT CODES
#ones: '1s'
#twos: '2s'
#threes: '3s'
#fours: '4s'
#fives: '5s'
#sixes: '6s'
#threek: '3k'
#fourk: '4k'
#fh: 'fh'
#smstr: 'ss'
#lgstr: 'ls'
#yaht: 'y'
#chan: 'c'

ones = "X"
twos = "X"
threes = "X"
fours = "X"
fives = "X"
sixes = "X"
top_score = "X"
top_bonus = "X"
top_total = "X"
threek = "X"
fourk = "X"
fh = "X"
smstr = "X"
lgstr = "X"
yaht = "X"
chan = "X"
yahtbo = 0
low_total = "X"
grand_total = "X"
randomlist = []

# Sets random die values and sets randomList
def set_random():
  global randomlist

  die1 = str(random.randint(1,6))
  die2 = str(random.randint(1,6))
  die3 = str(random.randint(1,6))
  die4 = str(random.randint(1,6))
  die5 = str(random.randint(1,6))

  randomlist = [die1, die2, die3, die4, die5]

  #Testing
  #randomlist = ['3','3','3','3','2']

def board():
  global ones, twos, threes, fours, fives, sixes, top_score, top_bonus, top_total, threek, fourk, fh, smstr, lgstr, yaht, chan, yahtbo, low_total, grand_total, randomlist

  print("UPPER SECTION")
  print("Aces:           | " + str(ones) + " |")
  print("Twos:           | " + str(twos) + " |")
  print("Threes:         | " + str(threes) + " |")
  print("Fours:          | " + str(fours) + " |")
  print("Fives:          | " + str(fives) + " |")
  print("Sixes:          | " + str(sixes) + " |")
  print("Total:          | " + str(top_score) + " |")
  print("63+ Bonus:      | " + str(top_bonus) + " |")
  print("Upper Total:    | " + str(top_total) + " |")
  
  print("LOWER SECTION")
  print("3 of a Kind:    | " + str(threek) + " |")
  print("4 of a Kind:    | " + str(fourk) + " |")
  print("Full House:     | " + str(fh) + " |")
  print("Sm Straight:    | " + str(smstr) + " |")
  print("Lg Straight:    | " + str(lgstr) + " |")
  print("YAHTZEE:        | " + str(yaht) + " |")
  print("Chance:         | " + str(chan) + " |")
  print("Yahtzee Bonus:  | " + str(yahtbo) + " |")
  print("Lower Total:    | " + str(low_total) + " |")
  print("Grand Total:    | " + str(grand_total) + " |\n")

  print("Codes: '1s', '2s', '3s', '4s', '5s', '6s', '3k', '4k', 'fh', 'ss', 'ls', 'y', 'c', 'x' (to zero)\n")
  
  print("Die 1    Die 2    Die 3    Die 4    Die 5\n ___      ___      ___      ___      ___\n| " + randomlist[0] + " |    | " + randomlist[1] + " |    | " + randomlist[2] + " |    | " + randomlist[3] + " |    | " + randomlist[4] + " |\n")

def top_full():
  global ones, twos, threes, fours, fives, sixes
  if "X" not in [ones, twos, threes, fours, fives, sixes]:
    return True
  else:
    return False

def low_full():
  global threek, fourk, fh, smstr, lgstr, yaht, chan
  if "X" not in [threek, fourk, fh, smstr, lgstr, yaht, chan]:
    return True
  else:
    return False

def check_full():
  global top_total, ones, twos, threes, fours, fives, sixes, top_score, top_bonus, low_total, threek, fourk, fh, smstr, lgstr, yaht, chan, yahtbo, grand_total

  #Sets the top total if the top is full
  if top_full() == True and top_total == "X":
      top_list = [ones, twos, threes, fours, fives, sixes]
      top_score = sum(top_list)
      if top_score >= 63:
        top_bonus = 35
      else:
        top_bonus = 0
      top_total = top_score + top_bonus
    
  #Sets the low total if the low is full
  if low_full() == True and low_total == "X":
    lower_list = [threek, fourk, fh, smstr, lgstr, yaht, chan, yahtbo]
    low_total = sum(lower_list)
    
  #Sets the grand total if both are full
  if top_full() == True and low_full() == True:
    grand_total = top_total + low_total

def invalid_numbers(parameter):
  invalid = 0
  for i in parameter:
    if int(i) > 5 or int(i) < 1:
      invalid += 1
  if invalid == 0:
    return False
  else:
    return True

def player_turn():
  global randomlist, rerolls

  clear()
  board()
  print("Rerolls: " + str(rerolls))

  #While you can reroll
  if rerolls >= 1:
    #REROLL or SCORE?
    question = input("Input 'r' to reroll or 's' to score: ")
    #REROLL
    if question == 'r':
      dice = input("Enter the die #s to reroll: ")
      #Valid input
      while len(dice) > 5 or invalid_numbers(dice) == True:
        dice = input("Enter valid die #s to reroll: ")
      #Reroll code 
      numeric_response_list = list(map(int, dice))
      for i in numeric_response_list:
        randomlist[i - 1] = str(random.randint(1,6))
      rerolls -= 1
      player_turn()
    #SCORE
    elif question == 's':
      scoring()
    #If neither, repeat question
    else:
      player_turn()
  #SCORE
  else:
    scoring()

def scoring():
  global randomlist, rerolls, ones, twos, threes, fours, fives, sixes, top_score, top_bonus, top_total, threek, fourk, fh, smstr, lgstr, yaht, chan, yahtbo, low_total, grand_total

  # Determine the count of each number
  ones_temp = 0
  twos_temp = 0
  threes_temp = 0
  fours_temp = 0
  fives_temp = 0
  sixes_temp = 0
  for i in randomlist:
    if i == '1':
      ones_temp += 1
    elif i == '2':
      twos_temp += 1
    elif i == '3':
      threes_temp += 1
    elif i == '4':
      fours_temp += 1
    elif i == '5':
      fives_temp += 1
    elif i == '6':
      sixes_temp += 1

  count_list = [ones_temp, twos_temp, threes_temp, fours_temp, fives_temp, sixes_temp]
  highest_count = count_list[0]
    
  # Determine the most common
  for i in count_list:
    if i > highest_count:
      highest_count = i

  #SPOT
  spot = input("Input the spot code to place your points ('x' to zero): ")
  #IS SPOT VALID? AND OPEN
  while spot not in ['x', '1s', '2s', '3s', '4s', '5s', '6s', '3k', '4k', 'fh', 'ss', 'ls', 'y', 'h', 'c'] or check_empty(spot, True) == False:
    if check_empty(spot, True) == False:
      print("You already have a value there. Try Again.")
      spot = input("Input a valid spot code to place your points ('x' to zero): ")
    else:
      spot = input("Input a valid spot code to place your points ('x' to zero): ")
  
  #ZERO OUT
  if spot == "x":
    #TOZERO INPUT
    tozero = input("Spot Code to zero: ")
    #IS TOZERO VALID?
    while tozero not in ["1s", "2s", "3s", "4s", "5s", "6s", "3k", "4k", "fh", "ss", "ls", "y", "c"] or check_empty(tozero, True) == False:
      if check_empty(tozero, True) == False:
        print("You already have a value there. Try Again.")
        tozero = input("Enter a valid Spot Code to zero: ")
      else:
        tozero = input("Enter a valid Spot Code to zero: ")
    variable_translate_set(tozero, 0)
  
  #Spot Code 1s, 2s, 3s, 4s, 5s, 6s
  elif spot in ["1s", "2s", "3s", "4s", "5s", "6s"]:
    num = spot[0]
    total = int(num) * randomlist.count(num)
    #VALIDATION
    if total == 0:
      print("You don't have any of that number. Try Again.")
      scoring()
    else:
        variable_translate_set(spot, total)

  #Spot Code 3k, 4k, c
  elif spot in ["3k", "4k", "c"]:
    #Totals all dice
    total = 0
    for i in randomlist:
      total += int(i)

    if spot == "3k":
      if highest_count < 3:
        print("You don't have three of the same number. Try Again.")
        scoring()
      else:
        threek = total

    elif spot == "4k":
      if highest_count < 4:
        print("You don't have four of the same number. Try again.")
        scoring()
      else:
        fourk = total

    elif spot == "c":
      chan = total
    else:
      print("Invalid Spot Code. Try again.")
      scoring()

  #FULL HOUSE
  elif spot == "fh":

    two_dice = False
    three_dice = False
    
    for i in count_list:
      if i == 2:
        two_dice = True
      elif i == 3:
        three_dice = True
      else:
        pass
    
    if two_dice and three_dice:
      fh = 25
    else:
      print("Your house is less than full. Try again.")
      scoring()
  
  #Small Straight
  elif spot == "ss":
    sequences = [['1','2','3','4'], ['2','3','4','5'], ['3','4','5','6']]
    if any(all(x in randomlist for x in seq) for seq in sequences):
      smstr = 30
    else:
      print("While small, thats not very straight. Try again.")
      scoring()
  
  #Large Straight
  elif spot == "ls":
    temp_sequences = [
        [ones_temp, twos_temp, threes_temp, fours_temp, fives_temp],
        [twos_temp, threes_temp, fours_temp, fives_temp, sixes_temp]
    ]
    if any(all(x == 1 for x in seq) for seq in temp_sequences):
      lgstr = 40
    else:
      print("Like most of your relationships, that's not going to work. Try again")
      scoring()
  
  #Yahtzee
  elif spot == "y":
    if len(set(randomlist)) == 1:
      if check_empty("y") == True:
        yaht = 50
      else:
        yahtbo += 100
    else:
      print("Thaaaat's disappointing. Try again.")
      scoring()
  else:
    print("Something went wrong. Try again.")
    scoring()
  
  check_full()

def variable_translate(passin):
    global ones, twos, threes, fours, fives, sixes, threek, fourk, fh, smstr, lgstr, yaht, chan
    if passin == "1s":
        return ones
    elif passin == "2s":
        return twos
    elif passin == "3s":
        return threes
    elif passin == "4s":
        return fours
    elif passin == "5s":
        return fives
    elif passin == "6s":
        return sixes
    elif passin == "3k":
        return threek
    elif passin == "4k":
        return fourk
    elif passin == "fh":
        return fh
    elif passin == "ss":
        return smstr
    elif passin == "ls":
        return lgstr
    elif passin == "y":
        return yaht
    elif passin == "c":
        return chan

def variable_translate_set(passin, value):
    global ones, twos, threes, fours, fives, sixes, threek, fourk, fh, smstr, lgstr, yaht, chan
    if passin == "1s":
        ones = value
    elif passin == "2s":
        twos = value
    elif passin == "3s":
        threes = value
    elif passin == "4s":
        fours = value
    elif passin == "5s":
        fives = value
    elif passin == "6s":
        sixes = value
    elif passin == "3k":
        threek = value
    elif passin == "4k":
        fourk = value
    elif passin == "fh":
        fh = value
    elif passin == "ss":
        smstr = value
    elif passin == "ls":
        lgstr = value
    elif passin == "y":
        yaht = value
    elif passin == "c":
        chan = value

def check_empty(passin, translate=False):
    global ones, twos, threes, fours, fives, sixes, threek, fourk, fh, smstr, lgstr, yaht, chan

    if translate:
        var = variable_translate(passin)
    else:
        var = passin

    if var != "X":
        return False
    else:
        return True
    
def zero_code(parameter):
  global ones, twos, threes, fours, fives, sixes, threek, fourk, fh, yaht, chan, smstr, lgstr
  

#Start Game
while grand_total == "X":
  rerolls = 2
  set_random()
  player_turn()

#End Game
clear()
board()
