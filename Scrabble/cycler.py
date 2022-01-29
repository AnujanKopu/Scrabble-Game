from itertools import cycle
from random import choice


class MyCycler():
    def __init__(self,player_list:list):
        self.cycle: cycle = cycle([i for i in range(len(player_list))])
        self.blacklist: set[str] = set()

    def add_to_blacklist(self,player_number:int):
        self.blacklist.add(player_number)

    def next_player(self):
        a = next(self.cycle)
        return a if a not in self.blacklist else self.blacklist.remove(a) or self.next_player()

    def get_first_player(self,player_list:list)->int:
        alphabetical_scores = [sum(ord(tile.letter.name if tile.letter.name != 'BLANK' else 'A') for tile in player.sprites) for player in player_list]
        lowest_score = min(alphabetical_scores)
        lowest_players = [index for index,element in enumerate(alphabetical_scores) if element == lowest_score]
    
        if len(lowest_players) == 1: 
            first_player = lowest_players[0]
        else: 
            first_player =choice(lowest_players)

        while True:
            if next(self.cycle) == first_player: return first_player






