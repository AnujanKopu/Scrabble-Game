import enum
from random import sample


class Character(enum.Enum): 
  BLANK=0
  A=1
  B=2
  C=3
  D=4
  E=5
  F=6
  G=7
  H=8
  I=9
  J=10
  K=11
  L=12
  M=13
  N=14
  O=15
  P=16
  Q=17
  R=18
  S=19
  T=20
  U=21
  V=22
  W=23
  X=24
  Y=25
  Z=26


class Bag():
    def __init__(self,num_of_bag=1):#Num of bag is 2 if there's 4 players
        self.dominos =  deque(sample([Character(index) for index,value in enumerate((2,9,2,2,4,12,2,3,2,9,1,1,4,2,6,8,2,1,6,4,6,4,2,2,1,2,1)) for _ in range(value*num_of_bag)],100*num_of_bag))

    def player_setup(self) -> tuple[Character,Character,Character,Character,Character,Character,Character]:
        return tuple(self.dominos.pop_left() for i in range(7))

    def grab_next(self)->Character:
        return self.dominos.pop_left()

    def extend_bag(self,character_list:list):
      while character_list: self.dominos.append(character_list.pop())
      self.dominos = deque(sample(self.dominos,len(self.dominos)))
      

class deque(list):
  def __getitem__(self,value):
    raise TypeError("'deque object is not subscriptable")

  def sort(self,value):
    raise  AttributeError("'deque' object has no attribute 'sort'")
  
  def append_Left(self,obj):
    self.insert(0,obj)

  def pop_left(self):
    return super().pop(0)
  
  def pop(self):
    return super().pop(-1)
  
  def peek_left(self):
    return super().__getitem__(0)

  def peek(self):
    return super().__getitem__(-1)

  

   