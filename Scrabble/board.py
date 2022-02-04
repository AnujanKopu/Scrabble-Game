import enum

from arcade import SpriteList,Sprite
from bag import Character
from word_checker import WordChecker

HORIZONTAL = False
VERTICAL = True

class NonLinearWord(Exception):
    def __init__(self):
        super().__init__('Characters are not alligned in a linear format(no diagonal)')
    

class Slot():

  def __init__(self,col:int,row:int):
    self.col:int = col
    self.row:int = row
    

  def __eq__(self,other):
    return hash(self) == hash(other)
    
  def __hash__(self):
    return hash((self.col,self.row))

  def __str__(self):
    return f"{self.col},{self.row}"


class Word():

  def __init__(self,col:int,row:int):
    self.beg:Slot = Slot(col,row)
    self.end:Slot = Slot(col,row)
    self.characters:list[Character] = []
    self.value:int = 0
    self.word_amp:int = 1

  def __str__(self):
      return "".join([i.name if i.name != "BLANK" else "_" for i in self.characters])

  def __dict__(self):
    return {'beg':(self.beg.col,self.beg.row),'end':(self.end.col,self.end.row),'characters':[i.name for i in self.characters],'value':self.value,'word_amp':self.word_amp}


class Play(): 

  def __init__(self,x,y):
    self.main_word:Word = Word(x,y)
    self.chains:list[Word] = []

  def get_points(self) -> int:
    return self.main_word.value*self.main_word.word_amp + sum([i.value*i.word_amp for i in self.chains])

  def __dict__(self):
    return {'main_word':self.main_word.__dict__(),'chains':[i.__dict__() for i in self.chains],'play_points':self.get_points()}


class Amplifier(enum.Enum):
    DOUBLEWORD = 1
    TRIPLEWORD = 2
    DOUBLELETTER = 3
    TRIPLELETTER = 4

class CharacterEvaluator():
    points_map:dict = {Character(0): 0,Character(1): 1, Character(5): 1, Character(9): 1, Character(12): 1, Character(14): 1, Character(15): 1, Character(18): 1, Character(19): 1, Character(20): 1, Character(21): 1, Character(4): 2, Character(7): 2, Character(2): 3, Character(3): 3, Character(13): 3, Character(16): 3, Character(6): 4, Character(8): 4, Character(22): 4, Character(23): 4, Character(25): 4, Character(11): 5, Character(10): 8, Character(24): 8, Character(17): 10, Character(26): 10}
    
    def __init__(self) -> None:
      self.first_play = True
      self.modifier_map: dict = {
        (1, 1): Amplifier(1), (2, 2): Amplifier(1), (3, 3): Amplifier(1), (4, 4): Amplifier(1), (13, 1): Amplifier(1), (12, 2): Amplifier(1), (11, 3): Amplifier(1), (10, 4): Amplifier(1), (10, 10): Amplifier(1), (11, 11): Amplifier(1), (12, 12): Amplifier(1), (13, 13): Amplifier(1), (4, 10): Amplifier(1), (3, 11): Amplifier(1), (2, 12): Amplifier(1), (1, 13): Amplifier(1),
        (14, 0): Amplifier(2), (7, 0): Amplifier(2), (0, 0): Amplifier(2), (0, 7): Amplifier(2), (0, 14): Amplifier(2), (7, 14): Amplifier(2), (14, 14): Amplifier(2), (14, 7): Amplifier(2),
        (11, 0): Amplifier(3), (8, 2): Amplifier(3), (7, 3): Amplifier(3), (6, 2): Amplifier(3), (3, 0): Amplifier(3), (0, 3): Amplifier(3), (14, 3): Amplifier(3), (12, 6): Amplifier(3), (8, 6): Amplifier(3), (6, 6): Amplifier(3), (2, 6): Amplifier(3), (3, 7): Amplifier(3), (11, 7): Amplifier(3), (12, 8): Amplifier(3), (8, 8): Amplifier(3), (6, 8): Amplifier(3), (2, 8): Amplifier(3), (0, 11): Amplifier(3), (14, 11): Amplifier(3), (7, 11): Amplifier(3), (8, 12): Amplifier(3), (6, 12): Amplifier(3), (11, 14): Amplifier(3), (3, 14): Amplifier(3),
        (5, 1): Amplifier(4), (9, 1): Amplifier(4), (13, 5): Amplifier(4), (9, 5): Amplifier(4), (5, 5): Amplifier(4), (1, 5): Amplifier(4), (1, 9): Amplifier(4), (5, 9): Amplifier(4), (9, 9): Amplifier(4), (13, 9): Amplifier(4), (9, 13): Amplifier(4), (5, 13): Amplifier(4)
      }
      self.remove_set:set[tuple[int,int]] = set()

    def get_word_points(self,col:int,row:int,letter:Character)-> tuple[int,int]:
        if self.first_play is True:
            self.first_play = False
            return (2,self.points_map[letter]) 
        if (col,row) in self.modifier_map: 
            amplifer = self.modifier_map[(col,row)]
            self.remove_set.add((col,row))
            if amplifer.value == 1: return (2,self.points_map[letter])
            elif amplifer.value == 2: return (3,self.points_map[letter])
            elif amplifer.value == 3: return (1,2*self.points_map[letter])
            elif amplifer.value == 3: return (1,3*self.points_map[letter])
        
        return (1,self.points_map[letter])

    def invalid_play(self)->None:
      self.remove_set.clear()


    def remove_modifers_after_play(self)->None:
      while self.remove_set:
        self.modifier_map.pop(self.remove_set.pop())

class Coords():
    def __init__(self,x=0,y=0):
        self.x:float = x
        self.y:float = y


class CurrentHand():
  def __init__(self):
    self.selected:set[Slot] = set()
    self.empty_origin:list[Coords] = []
    self.held:Sprite = None
    self.held_origin:Coords = Coords()

class Board():
    def __init__(self) -> None:
      self.board: list = [[None for i in range(15)] for i in range(15)]
      self.board_tiles:SpriteList = SpriteList()
      self.coord_map:set[tuple[Slot]] = set()
      self.charcter_evaluator: CharacterEvaluator = CharacterEvaluator()
      self.word_checker = WordChecker()

    def add_tiles(self,tiles:SpriteList)->None:
      self.board_tiles.extend(tiles)

    def place_on_board(self,col:int,row:int,character:Character)-> None:
        self.board[col][row] = character
        
    def swap_on_board(self,col1:int,row1:int,col2:int,row2:int)->None:
        self.board[col1][row1],self.board[col2][row2] = self.board[col2][row2],self.board[col1][row1] 

    def slot_used(self,col,row)->bool:
      return True if not self.board[col][row] is None else False

    def validate_slot(self,col,row,beside_itself=False)->None:

      number_of_tiles_needed = 1 if beside_itself is False else 2
      if self.board[7][7] is None: return True if col == 7 and row == 7 else False 

      for x,y in ((0,1),(1,0),(0,-1),(-1,0)):
        if col+x >= 0 and col+x < 15 and row+y >= 0 and row+y < 15:
          if not self.board[col+x][row+y] is None: 
              number_of_tiles_needed -= 1
              if number_of_tiles_needed == 0: return True

      return False


    def get_main_direction(self,first_tile_coords:Slot,second_tile_coords:Slot)-> bool:

        if (first_tile_coords.col ==second_tile_coords.col) ^ (first_tile_coords.row==second_tile_coords.row):
            if first_tile_coords.col==second_tile_coords.col: return VERTICAL
            elif first_tile_coords.row==second_tile_coords.row: return HORIZONTAL
            else: return None

    def add(self,col:int,row:int,word:Word)-> None:
        word.characters.append(self.board[col][row])
        word_amp,points = self.charcter_evaluator.get_word_points(col,row,word.characters[-1]) 
        word.word_amp *= word_amp
        word.value += points
        

    def addleft(self,col:int,row:int,word:Word) -> None:
        word.characters.insert(0,self.board[col][row])
        word_amp,points = self.charcter_evaluator.get_word_points(col,row,word.characters[0]) 
        word.word_amp *= word_amp
        word.value += points
        

    def get_words(self,selected_copy:set,direction:bool,y:int,x:int)-> Play: 
        self.charcter_evaluator.remove_modifers_after_play()
        result = Play(y,x)

       
        if direction is True:
          for i in range(x,-1,-1):
           
            
            if self.board[y][i] is None: 
              result.main_word.beg = Slot(y,i+1)
              break
            if i == 0:
              result.main_word.beg = Slot(y,i)
            

            self.add(y,i,result.main_word)
              
  
            if (y,i) in selected_copy:
              temp = Word(y,i)
              
              for j in range(y-1,-1,-1):
                
                if self.board[j][i] is None: 
                  temp.beg = Slot(j+1,i)
                  break
                if j == 0:
                  temp.beg = Slot(j,i)
                self.addleft(j,i,temp)
              

              for j in range(y,len(self.board)):
                if self.board[j][i] is None: 
                  temp.end = Slot(j-1,i)
                  break
                if j == len(self.board)-1:
                  temp.end = Slot(j,i)
                self.add(j,i,temp)
               
                

              if len(temp.characters) > 1: 
                if (temp.beg,temp.end) not in self.coord_map:
                  result.chains.append(temp)
                  self.coord_map.add((temp.beg,temp.end))

              selected_copy.remove((y,i))

 
          for i in range(x+1,len(self.board[y])):
     
            if self.board[y][i] is None: 
              result.main_word.end = Slot(y,i-1)
              break
            if i == len(self.board)-1:
              result.main_word.end = Slot(y,i)
          

            self.addleft(y,i,result.main_word)
          
            if (y,i) in selected_copy:
              temp = Word(y,i)
              for j in range(y-1,-1,-1):
                if self.board[j][i] is None: 
                  temp.beg = Slot(j+1,i)
                  break
                if j == 0:
                  temp.beg = Slot(j,i)
                self.addleft(j,i,temp) 


         
              for j in range(y,len(self.board)):
                if self.board[j][i] is None: 
                  temp.end = Slot(j-1,i)
                  break
                if j == len(self.board)-1:
                  temp.end = Slot(j,i)
                self.add(j,i,temp)



              if len(temp.characters) > 1: 
                if (temp.beg,temp.end) not in self.coord_map:
                  result.chains.append(temp)
                  self.coord_map.add((temp.beg,temp.end))
              
              selected_copy.remove((y,i))

        else:
          for i in range(y+1,len(self.board)):
            if self.board[i][x] is None: 
              result.main_word.end = Slot(i-1,x)
              break
            if i == len(self.board)-1:
              result.main_word.end = Slot(i,x)
              
            self.add(i,x,result.main_word)


            if (i,x) in selected_copy:
              temp = Word(i,x)
              for j in range(x+1,len(self.board[i])):
                  if self.board[i][j] is None:
                      temp.end = Slot(i,j-1)
                      break
                  if j ==len(self.board[i])-1:
                      temp.end = Slot(i,j)
                  self.addleft(i,j,temp)
  
                  


              for j in range(x,-1,-1):
                  if self.board[i][j] is None:
                      temp.beg = Slot(i,j+1)
                      break
                  if j == 0:
                      temp.beg = Slot(i,j) 
                  self.add(i,j,temp)


              if len(temp.characters) > 1: 
                if (temp.beg,temp.end) not in self.coord_map:
                  result.chains.append(temp)
                  self.coord_map.add((temp.beg,temp.end))
              

              selected_copy.remove((i,x))


          for i in range(y,-1,-1):
            if self.board[i][x] is None: 
              result.main_word.beg = Slot(i+1,x)
              break
            if i == 0:
              result.main_word.beg = Slot(i,x)
              
            self.addleft(i,x,result.main_word) 

            
            if (i,x) in selected_copy:
              temp = Word(i,x)
              for j in range(x+1,len(self.board[i])):
                  if self.board[i][j] is None:
                      temp.end = Slot(i,j-1)
                      break
                  if j ==len(self.board[i])-1:
                      temp.end = Slot(i,j)
                  
                  self.addleft(i,j,temp)


              for j in range(x,-1,-1):
                  if self.board[i][j] is None:
                      temp.beg = Slot(i,j+1)
                      break
                  if j == 0:
                      temp.beg = Slot(i,j) 
                      
                  self.add(i,j,temp)

                  
              
              if len(temp.characters) > 1: 
                if (temp.beg,temp.end) not in self.coord_map:
                  result.chains.append(temp)
                  self.coord_map.add((temp.beg,temp.end))

              selected_copy.remove((i,x))
            
        
        return result

  
    
    def clean_word_map_of_invalid_play(self,words:Play)->None:
      self.charcter_evaluator.invalid_play()

      for i in words.chains:
          self.coord_map.remove((i.beg,i.end))

    

    def evaluate_play(self,selected_copy:set[Slot])->Play:
        a,b = selected_copy.pop(),selected_copy.pop()
        selected_copy.update([b,a])

        direction = self.get_main_direction(a,b)
        if direction is None: raise NonLinearWord

        words = self.get_words(selected_copy,direction,a.col,a.row)
        if len(selected_copy) != 0:raise NonLinearWord
        return words



