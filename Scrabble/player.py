import imp
from arcade import SpriteList
from board import Play
from dataclasses import dataclass,field


@dataclass
class Player():
    name:str
    sprites: SpriteList
    points:int = field(default_factory=0)
    words:list[Play] = field(default_factory=[])

    #def __hash__(self):
        #return hash(self.name)


