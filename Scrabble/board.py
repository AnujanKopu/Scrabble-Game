

class NotWordError(Exception):
  def __init__(self,value):
    self.value = value
    self.message = f"Characters at {value} not alligned with rest of the word"
    super().__init__(self.message)


class Coords():
  x = 0
  y = 0

class CurrentHand():
  selected = set()
  held = None
  held_origin = Coords()
  empty_origin = []

class Board():
  def __init__(self,board):
    self.board = board
    self.modifer_map = {
      (1, 1): 'DW', (2, 2): 'DW', (3, 3): 'DW', (4, 4): 'DW', (13, 1): 'DW', (12, 2): 'DW', (11, 3): 'DW', (10, 4): 'DW', (10, 10): 'DW', (11, 11): 'DW', (12, 12): 'DW', (13, 13): 'DW', (4, 10): 'DW', (3, 11): 'DW', (2, 12): 'DW', (1, 13): 'DW',
      (14, 0): 'TW', (7, 0): 'TW', (0, 0): 'TW', (0, 7): 'TW', (0, 14): 'TW', (7, 14): 'TW', (14, 14): 'TW', (14, 7): 'TW',
      (11, 0): 'DL', (8, 2): 'DL', (7, 3): 'DL', (6, 2): 'DL', (3, 0): 'DL', (0, 3): 'DL', (14, 3): 'DL', (12, 6): 'DL', (8, 6): 'DL', (6, 6): 'DL', (2, 6): 'DL', (3, 7): 'DL', (11, 7): 'DL', (12, 8): 'DL', (8, 8): 'DL', (6, 8): 'DL', (2, 8): 'DL', (0, 11): 'DL', (14, 11): 'DL', (7, 11): 'DL', (8, 12): 'DL', (6, 12): 'DL', (11, 14): 'DL', (3, 14): 'DL',
      (5, 1): 'TL', (9, 1): 'TL', (13, 5): 'TL', (9, 5): 'TL', (5, 5): 'TL', (1, 5): 'TL', (1, 9): 'TL', (5, 9): 'TL', (9, 9): 'TL', (13, 9): 'TL', (9, 13): 'TL', (5, 13): 'TL'
      }
    self.points_map = {'a': 1, 'e': 1, 'i': 1, 'l': 1, 'n': 1, 'o': 1, 'r': 1, 's': 1, 't': 1, 'u': 1, 'd': 2, 'g': 2, 'b': 3, 'c': 3, 'm': 3, 'p': 3, 'f': 4, 'h': 4, 'v': 4, 'w': 4, 'y': 4, 'k': 5, 'j': 8, 'x': 8, 'q': 10, 'z': 10}
    self.word_map = set()

    
  def get_words(self,selected:set):#Provide DeepCopy Selected. 
    class Word():
      word:str = ''
      beg:tuple 
      end:tuple 
      value:int = 0
      word_amp:int = 1
      letter_amp:int = 0
 
      def get_value(self):
        return (self.value + self.letter_amp)*self.word_amp



    class Result():
      main_word:Word = Word()
      chains:list = []
    

    #Need to do comparison between two tuples to find main direction
    a,b = selected.pop(),selected.pop()
    if(a[0] == b[0]) ^ (a[1] == b[1]):
        selected.update([b,a])
        result = Result()
        y,x = a[0],a[1]
        temp = Word()


        #Depending on direction, find chaining words in other axis. 
        if a[0] == b[0]:
          for i in range(x,-1,-1):
            
                
            if self.board[y][i] is None: 
              result.main_word.beg = (y,i+1)
              break
            if i == 0:
              result.main_word.beg = (y,i)
            
            result.main_word.word = self.board[y][i] + result.main_word.word
            self.evaluate_points(result.main_word,(y,i))
              

            if (y,i) in selected:

              for j in range(y-1,-1,-1):
                if self.board[j][i] is None: 
                  temp.beg = (j+1,i)
                  break
                if j == 0:
                  temp.beg = (j,i)
                temp.word = self.board[j][i] + temp.word
                self.evaluate_points(temp,(j,i))

              for j in range(y,len(self.board)):
                if self.board[j][i] is None: 
                  temp.end = (j-1,i)
                  break
                if j == len(self.board)-1:
                  temp.end = (j,i)
                temp.word += self.board[j][i]
                self.evaluate_points(temp,(j,i))
                

              if temp.word: 
                if (temp.word.beg,temp.word.end) not in self.word_map:
                  result.chains.append(temp)
                  self.word_map.add((temp.word.beg,temp.word.end))

                temp = Word()
              selected.remove((y,i))

          for i in range(x+1,len(self.board[y])):
            
            if self.board[y][i] is None: 
              result.main_word.end = (y,i-1)
              break
            if i == len(self.board)-1:
              result.main_word.end = (y,i)
          
            result.main_word.word += self.board[y][i]
            self.evaluate_points(result.main_word,(y,i))

            if (y,i) in selected:

              for j in range(y-1,-1,-1):
                if self.board[j][i] is None: 
                  temp.beg = (j+1,i)
                  break
                if j == 0:
                  temp.beg = (j,i)
                temp.word = self.board[j][i] + temp.word
                self.evaluate_points(temp,(j,i))


              for j in range(y,len(self.board)):
                if self.board[j][i] is None: 
                  temp.end = (j-1,i)
                  break
                if j == len(self.board)-1:
                  temp.end = (j,i)
                temp.word += self.board[j][i]
                self.evaluate_points(temp,(j,i))


              if temp.word: 
                if (temp.word.beg,temp.word.end) not in self.word_map:
                  result.chains.append(temp)
                  self.word_map.add((temp.word.beg,temp.word.end))
                temp = Word()
              selected.remove((y,i))

        else:

          for i in range(y+1,len(self.board)):
            if self.board[i][x] is None: 
              result.main_word.end = (i-1,x)
              break
            if i == len(self.board)-1:
              result.main_word.end = (i,x)
              
            result.main_word.word += self.board[i][x]
            self.evaluate_points(result.main_word,(i,x))


            if (i,x) in selected:
              for j in range(x+1,len(self.board[i])):
                  if self.board[i][j] is None:
                      temp.end = (i,j-1)
                      break
                  if j ==len(self.board[i])-1:
                      temp.end = (i,j)
                  temp.word += self.board[i][j]
                  self.evaluate_points(temp,(i,j))
                  


              for j in range(x,-1,-1):
                  if self.board[i][j] is None:
                      temp.beg = (i,j+1)
                      break
                  if j == 0:
                      temp.beg = (i,j) 
                  temp.word = self.board[i][j] + temp.word
                  self.evaluate_points(temp,(i,j))

              if temp.word: 
                if (temp.word.beg,temp.word.end) not in self.word_map:
                  result.chains.append(temp)
                  self.word_map.add((temp.word.beg,temp.word.end))
                temp = Word()
              selected.remove((i,x))


          for i in range(y,-1,-1):
            if self.board[i][x] is None: 
              temp.beg = (i+1,x)
              break
            if i == 0:
              temp.beg = (i,x)
              
            result.main_word.word = self.board[i][x] +  result.main_word.word
            self.evaluate_points(result.main_word,(i,x))
            

            if (i,x) in selected:
              for j in range(x+1,len(self.board[i])):
                  if self.board[i][j] is None:
                      temp.end = (i,j-1)
                      break
                  if j ==len(self.board[i])-1:
                      temp.end = (i,j)
                  
                  temp.word += self.board[i][j]
                  self.evaluate_points(temp,(i,j))

              for j in range(x,-1,-1):
                  if self.board[i][j] is None:
                      temp.beg = (i,j+1)
                      break
                  if j == 0:
                      temp.beg = (i,j) 
                      
                  temp.word = self.board[i][j] + temp.word
                  self.evaluate_points(temp,(i,j))
                  
              
              if temp.word: 
                if (temp.word.beg,temp.word.end) not in self.word_map:
                  result.chains.append(temp)
                  self.word_map.add((temp.word.beg,temp.word.end))

                temp = Word()
              selected.remove((i,x))


        if len(selected):
          raise NotWordError(selected)
        else:
          #return result
          print(result.main_word.word)
          for word in result.chains:
            print(word.word,word.beg,word.end)
    else:
      raise NotWordError()


  def evaluate_points(self,word,coords:tuple):
    word.value += self.points_map[coords[0]][coords[1]]
    if coords in self.modifer_map:
      if self.modifer_map[coords] == 'DW':
        word.word_amp *= 2
      elif self.modifer_map[coords] == 'TW':
        word.word_amp *= 3
      elif self.modifer_map[coords] == 'DL':
        word.letter_amp += self.points_map[self.board[coords[0]][coords[1]]]
      elif  self.modifer_map[coords] == 'TL':
        word.letter_amp += self.points_map[self.board[coords[0]][coords[1]]]*2


  
        

        


    

