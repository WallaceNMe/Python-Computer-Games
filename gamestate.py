from cards import mortals_list, special_dragons_list, deck_list, name_list, traditional_mortals_list

# Colors
    #self.GREEN_BG = '\033[42m\033[30m\033[1m'
    #self.RED_BG = '\033[41m\033[30m\033[1m'
    #self.BLUE_BG = '\033[44m\033[30m\033[1m'
    #self.CYAN_BG = '\033[46m\033[30m\033[1m'
    #self.WHITE_BG = '\033[47m\033[30m\033[1m'
    #self.BRIGHT_RED_BG = '\033[101m\033[30m\033[1m'
    #self.BRIGHT_GREEN_BG = '\033[102m\033[30m\033[1m'
    #self.BRIGHT_BLUE_BG = '\033[104m\033[30m\033[1m'
    #self.BRIGHT_CYAN_BG = '\033[106m\033[30m\033[1m'
    #self.BRIGHT_WHITE_BG = '\033[107m\033[30m\033[1m'
    #self.BLUE_BG_WHITE = '\033[44m\033[37m\033[1m'
    #self.RED_BG_WHITE = '\033[41m\033[37m\033[1m'
    #self.MAGENTA_BG_WHITE = '\033[45m\033[37m\033[1m'   

class GameState():
  # g.var_name
  def __init__(self): 
    self.YELLOW_BG = '\033[43m\033[30m\033[1m'
    self.GRAY_BG = '\033[100m\033[37m\033[1m'
    self.RESET = '\033[0m'
    self.MAGENTA_BG = '\033[45m\033[30m\033[1m'
    self.BRIGHT_MAGENTA_BG = '\033[105m\033[30m\033[1m'
    self.BRIGHT_YELLOW_BG = '\033[103m\033[30m\033[1m'
    # Variables
    self.player_count = None
    self.starting_gold = 0
    self.user_name = None
    self.mortals_list = mortals_list
    self.special_dragons_list = special_dragons_list
    self.traditional_mortals_list = traditional_mortals_list
    self.deck_list = deck_list
    self.draw_pile = []
    self.discard_pile = []
    self.ante_pile = []
    self.name_list = name_list
    self.picked_cards = []
    self.player_list = []
    self.stakes = 0
    self.round_leader = None
    self.gambit_number = 0
    self.rounds = [1, 2, 3]
    self.round_events = []
    self.loser = False
    self.round_front_runner = None
    self.current_round = 0

g = GameState()