class Card():
  def __init__(self, name, strength, alignment, power, colors):
    self.name = name
    self.strength = strength
    self.alignment = alignment
    self.power = power
    self.colors = colors
  
  def __repr__(self):
    return self.name

# MORTALS
the_archmage = Card("The Archmage 9", 9, "Mortal", "All cards you play later this gambit trigger their powers.", ["Mortal"])
the_dragonrider = Card("The Dragonrider 6", 6, "Mortal", "When this gambit is scored, the strength of this card equals the strength of the weakest dragon in your flight, not this card's printed strength.", ["Mortal"])
the_dragonslayer = Card("The Dragonslayer 8", 8, "Mortal", "Discard a weaker dragon from any flight.", ["Mortal"])
the_druid = Card("The Druid 6", 6, "Mortal", "The player with the weakest flight wins the gambit instead of the player with the strongest flight.", ["Mortal"])
the_fool = Card("The Fool 3", 3, "Mortal", "Draw a card for each opponent with a flight stronger than yours.", ["Mortal"])
the_illusionist = Card("The Illusionist 4", 4, "Mortal", "You can swap this card with a ortal in an opponent's flight. If you do, your new mortal triggers its power regardless of its strength.", ["Mortal"])
the_kobold = Card("The Kobold 2", 2, "Mortal", "Discard as many cards as you wish from your hand. Then draw that many cards.", ["Mortal"])
the_merchant_prince = Card("The Merchant Prince 5", 5, "Mortal", "Until the end of this gambit, any gold players would put into the stakes to buy new cards goes to you instead of into the stakes.", ["Mortal"])
the_priest = Card("The Priest 5", 5, "Mortal", "The winner of the gambit splits the stakes with the player to their left.", ["Mortal"])
the_princess = Card("The Princess 4", 4, "Mortal", "The power of each good dragon in your flight triggers.", ["Mortal"])
the_prophet = Card("The Prophet 10", 10, "Mortal", "You can reveal a dragon in your hand and trigger its power as if the Prophet had triggered the power.", ["Mortal"])
the_queen = Card("The Queen 7", 7, "Mortal", "Each opponent with both good and evil dragons in the same flight pays you 5 gold, and you take a random card from that player's hand.", ["Mortal"])
the_sorcerer = Card("The Sorcerer 8", 8, "Mortal", "Reveal the top three cards of the deck. Discard this card and replace it with one of the revealed cards. That card's power triggers. Put the other two revealed cards into the ante.", ["Mortal"])
the_thief = Card("The Thief 7", 7, "Mortal", "Steal 7 gold from the stakes.", ["Mortal"])
the_wyrmpriest = Card("The Wyrmpriest 5", 5, "Mortal", "For the rest of the gambit, this card counts as any color for completing a color flight.", ["Mortal"])

# SPECIAL DRAGONS
bahamut = Card("Bahamut 13", 13, "Good", "Dragon god--As long as you have Bahamut and an evil dragon in your flight, you can't win the gambit. Power: Each other player with both good and evil dragons in the same flight pays you 10 gold.", ["Gold", "Silver", "Bronze", "Copper", "Brass"])
black_raider = Card("Black Raider 8", 8, "Evil", "Steal 1 gold from the stakes, then take 2 gold from the opponent to your left, 3 gold from the opponent to their left, and so on until you have taken gold from everyone.", ["Black"])
blue_overlord = Card("Blue Overlord 10", 10, "Evil", "Choose one: Each opponent gives you 2 gold OR each opponent adds 2 gold to the stakes for each card in your flight.", ["Blue"])
brass_sultan = Card("Brass Sultan 8", 8, "Good", "The opponents to your left and right each choose either to give you a stronger good dragon from their hand or to pay you 5 gold.", ["Brass"])
bronze_warlord = Card("Bronze Warlord 10", 10, "Good", "Take the two weakest cards from the ante. Then if you do not win the gambit after the third round, play a fourth round.", ["Bronze"])
chromatic_wyrmling = Card("Chromatic Wyrmling 1", 1, "Evil", "You may discard this card and replace it with an evil dragon from your hand. The new card's power triggers regardless of its strength.", ["Black", "Blue", "Green", "Red", "White"])
copper_trickster = Card("Copper Trickster 9", 9, "Good", "Discard a different card in your flight and replace it with the top card of the deck. You can trigger the new card's power if you wish.", ["Copper"])
dracolich = Card("Dracolich 10", 10, "Evil", "When the gambit is scored, you get +2 Strength for each dragon in your flight.", ["Colorless"])
gold_monarch = Card("Gold Monarch 12", 12, "Good", "Draw a card for each good dragon in your flight. Then if you win this gambit, gift each opponent 3 gold.", ["Gold"])
green_schemer = Card("Green Schemer 5", 5, "Evil", "The opponents to your left and right each choose either to give you a weaker evil dragon from their hand or to pay you 5 gold.", ["Green"])
metallic_wyrmling = Card("Metallic Wyrmling 1", 1, "Good", "You may discard this card and replace it with a good dragon from your hand. The new card's power triggers regardless of its strength.", ["Gold", "Silver", "Bronze", "Copper", "Brass"])
red_destroyer = Card("Red Destroyer 11", 11, "Evil", "The opponent with the strongest flight pays you 10 g0ld. Take a random card from that player's hand.", ["Red"])
silver_seer = Card("Silver Seer 11", 11, "Good", "Each player with at least one good dragon in their flight draws a card, then you look at the top three cards of the deck, choose one, and discard the others. ", ["Silver"])
tiamat = Card("Tiamat 13", 13, "Evil", "Dragon god--Tiamat counts as a Black, Blue, Green, Red, and White Dragon. As long as you have Tiamat and a good dragon in your flight, you can't win the gambit.", ["Black", "Blue", "Green", "Red", "White"])
white_hunter = Card("White Hunter 7", 7, "Evil", "Each weaker opponent pays you 3 gold.", ["White"])

mortals_list = [the_archmage, the_dragonrider, the_dragonslayer, the_druid, the_fool, the_illusionist, the_kobold, the_merchant_prince, the_priest, the_princess, the_prophet, the_queen, the_sorcerer, the_thief, the_wyrmpriest]

special_dragons_list = [bahamut, black_raider, blue_overlord, brass_sultan, bronze_warlord, chromatic_wyrmling, copper_trickster, dracolich, gold_monarch, green_schemer, metallic_wyrmling, red_destroyer, silver_seer, tiamat, white_hunter]

traditional_mortals_list = [the_archmage, bahamut, dracolich, the_dragonslayer, the_druid, the_fool, the_priest, the_princess, the_thief, tiamat]

deck_list = []
# Black
for number in [1,2,3,5,6,7,9]:
  black_dragon = Card(f"Black {number}", number, "Evil", "Steal 3 gold from the stakes.", ["Black"])
  deck_list.append(black_dragon)
# Blue
for number in [1,2,4,6,7,9,11]:
  blue_dragon = Card(f"Blue {number}", number, "Evil", "Choose one: Each opponent gives you 1 gold or each opponent adds 1 gold to the stakes for each chard in your flight.", ["Blue"])
  deck_list.append(blue_dragon)
# Brass
for number in [1,2,3,4,5,7,9]:
  brass_dragon = Card(f"Brass {number}", number, "Good", "The opponent to your right chooses either to give you a stronger good dragon from their hand or to pay you 5 gold.", ["Brass"])
  deck_list.append(brass_dragon)
# Bronze
for number in [1,3,6,7,8,9,11]:
  bronze_dragon = Card(f"Bronze {number}", number, "Good", "Take the two weakest cards from the ante.", ["Bronze"])
  deck_list.append(bronze_dragon)
# Copper
for number in [1,3,5,6,7,8,10]:
  copper_dragon = Card(f"Copper {number}", number, "Good", "Discard this card and replace it with the top card of the deck. That card's power triggers regardless of its strength.", ["Copper"])
  deck_list.append(copper_dragon)
# Gold
for number in [2,4,6,8,9,11,13]:
  gold_dragon = Card(f"Gold {number}", number, "Good", "Draw a card for each good dragon in your flight.", ["Gold"])
  deck_list.append(gold_dragon)
# Green
for number in [1,2,4,5,6,8,10]:
  green_dragon = Card(f"Green {number}", number, "Evil", "The opponent to your left chooses either to give you a weaker evil dragon from their hand or to pay you 5 gold.", ["Green"])
  deck_list.append(green_dragon)
# Red
for number in [2,3,5,7,8,10,12]:
  red_dragon = Card(f"Red {number}", number, "Evil", "The opponent with the strongest flight pays you 1 gold. Take a random card from that player's hand.", ["Red"])
  deck_list.append(red_dragon)
# Silver
for number in [2,3,6,7,8,10,12]:
  silver_dragon = Card(f"Silver {number}", number, "Good", "Each player with at least one good dragon in their hand draws a card.", ["Silver"])
  deck_list.append(silver_dragon)
# White
for number in [1,2,3,4,5,6,8]:
  silver_dragon = Card(f"White {number}", number, "Evil", "The weakest Opponent pays you 2 gold", ["White"])
  deck_list.append(silver_dragon)

name_list = [
    # Human names
    "Aldric Thornheart",
    "Mira Blackwood",
    "Gareth Ironfoot",
    "Elara Moonwhisper",
    "Thorne Greystone",
    
    # Elf names
    "Faelwen Silverleaf",
    "Thalion Starweaver",
    "Lysandra Dawnbringer",
    "Aelar Windwhisper",
    "Silaqui Nightshade",
    
    # Dwarf names
    "Thorin Ironbeard",
    "Brenna Stoneforge",
    "Balin Hammerfall",
    "Gilda Deepdelver",
    "Kromm Firestone",
    
    # Halfling names
    "Pippin Goodbarrel",
    "Rosie Underhill",
    "Merric Tosscobble",
    "Lidda Tealeaf",
    "Finnegan Brushgather",
    
    # Dragonborn names
    "Kriv Thunderscale",
    "Sora Flameheart",
    "Balasar Ironclaw",
    "Mishann Emberwing",
    "Torinn Goldbreath",
    
    # Tiefling names
    "Zariel Nightshade",
    "Virtue Ashenblade",
    "Morthos Shadowhorn",
    "Akta Hellfire",
    "Nemeia Darkwhisper",
    
    # Half-Orc names
    "Grommash Skullcrusher",
    "Yevelda Ironhide",
    "Thokk Bloodfang",
    "Krazka Bonegrinder",
    "Gorzak Steelfist",
    
    # Gnome names
    "Bimpnoddle Tinkertop",
    "Zanna Sparklegem",
    "Fibblestib Cogsworth",
    "Nyx Quickfingers",
    "Jebeddo Moonwhirl",
    
    # Half-Elf names
    "Aramil Silvermoon",
    "Liara Softwind",
    "Talos Brightwood",
    "Shiera Ravenshadow",
    "Eryndor Stormborn"
]