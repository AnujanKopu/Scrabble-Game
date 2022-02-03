from arcade import SpriteList


class Player():
    def __init__(self,name:str,tiles:SpriteList):
        self.name:str = name
        self.sprites:SpriteList = tiles
        self.points:int =0
        self.words:list = []
        

    def __hash__(self):
        return hash(self.name)


