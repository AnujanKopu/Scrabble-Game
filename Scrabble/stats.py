from player import Player
from datetime import date, datetime
import pytz
from dataclasses import dataclass,field,asdict
from os import environ

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

is_on = True
try:
    cluster = MongoClient(environ['MONGOKEY'])
    db = cluster['ScrabbleGames']
    collection = db['Games']
except ConnectionFailure as e:
    print(e)
    is_on = False

    
    
def is_connected_to_db() -> bool:
    return is_on

@dataclass
class GameStats():
    players:list[Player]
    num_of_challenges:int = field(default_factory=0)
    num_of_shuffles:int = field(default_factory=0)
    num_of_plays:int = field(default_factory=0)
    dt:datetime = field(default_factory=datetime.now())


def save_stats(game_stats:GameStats):
    """
    for i in game_stats.players:
        for j in i.words:
            j.main_word.characters = [i.name for i in j.main_word.characters]
            for k in j.chains:
                    k.characters = [i.name for i in k.characters]
    """
    
    collection.insert_one(asdict(game_stats))



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
      found = list(collection.find({'tme':{"$gt":dt,"$lt":edt}}))
      if len(found) > 0:
        for i in found:
          i['dt'] = i['dt'].astimezone(pytz.timezone('US/Eastern'))
      return  found


