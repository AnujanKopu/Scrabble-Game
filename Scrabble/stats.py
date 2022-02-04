from player import Player
from datetime import date, datetime
import pytz
from dataclasses import dataclass,asdict
from os import environ

from pymongo.errors import ConnectionFailure,ConfigurationError

is_on = True
try:
    from pymongo import MongoClient
    cluster = MongoClient(environ['MONGOKEY'])
    db = cluster['ScrabbleGames']
    collection = db['Games']
except (ConnectionFailure,ConfigurationError) as e:
    print(e)
    is_on = False

    
    
def is_connected_to_db() -> bool:
    return is_on

@dataclass
class GameStats():
    players:list[Player]
    num_of_challenges:int = 0
    num_of_shuffles:int = 0
    num_of_plays:int = 0
    dt:datetime = datetime.now()



        


def save_stats(game_stats:GameStats,if_word_stats:bool,if_action_stats:bool):
    if not (if_word_stats is False and if_action_stats is False):
        for players in game_stats.players:
            players.sprites = None
            for i in range(len(players.words)):
                players.words[i] = players.words[i].__dict__()
        sdict = asdict(game_stats)

        
        for players in sdict['players']:
            del players['sprites']

        if if_word_stats is False: del sdict['players']
        elif if_action_stats is False:
            del sdict['num_of_plays']
            del sdict['num_of_shuffles'] 
            del sdict['num_of_challenges']

        collection.insert_one(sdict)



class InfoError(Exception):

  def __init__(self,message:str) -> None:
    self.message = message
    super().__init__(message)

def make_query(date_string:str):
      if date_string == 'default':
          dt = datetime.today()
          date_string = f'{dt.year}//{dt.month}//{dt.day}'
      date_string = date_string.split("/",2)
      if len(date_string) == 3:
        if date_string[0].isdigit() and date_string[1].isdigit() and date_string[2].isdigit():
          year = int(date_string[0])
          month = int(date_string[1])
          day = int(date_string[2])
          dt = datetime(year,month,day)
          edt = datetime(year,month,day+1)
      elif len(date_string) == 2:
        if date_string[0].isdigit() and date_string[1].isdigit():
          year = int(date_string[0])
          month = int(date_string[1])
          dt = datetime(year,month,1)
          edt = datetime(year,month+1,1)
      else:
        raise InfoError("Invalid date: YYYY/MM/Optional[DD]")
      found = list(collection.find({'dt':{"$gt":dt,"$lt":edt}}))
      if len(found) > 0:
        for i in found:
          i['dt'] = i['dt'].astimezone(pytz.timezone('US/Eastern'))

      return  found


