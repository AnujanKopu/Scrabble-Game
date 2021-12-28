
from pyglet.window.key import C, P
from bag import Bag
from copy import deepcopy
from board import Board,CurrentHand,NotWordError
from config import *
from tiles import make_letters

from enum import Enum
from itertools import cycle,groupby

import arcade
from arcade.gui import UIManager,UITextureButton


class Coords():
  x = 0
  y = 0

class GameState(Enum):
  Setup = 0
  Title = 1
  Game = 2



class Tile(arcade.Sprite):

  def __init__(self,player,letter,args):
    super().__init__(filename=f'./Scrabble/tiles/{letter.name}.png',scale=1,**args)
    #self.player = player
    #$self.letter = letter
  



class Display(arcade.Window):

    def __init__(self):
        # Setup the window by initializing the parent class
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

      
        self.manager = UIManager()
        self.manager.enable()
        
        submit_btn = UITextureButton(texture=arcade.load_texture('./Scrabble/textures/submit.png'), width=150 ,height=100)
        self.manager.add(submit_btn)

      


        self.Bag = Bag()
        self.Bag.create()
        self.board = Board(board)


        self.State = GameState(0)
        self.players = ["Andrew","Matt","Sally","Johnny"]
        self.current_player = 0
        self.player_create(["Andrew","Matt","Sally","Johnny"])
        self.hand = CurrentHand()
        self.mouseoffset = Coords()
  

        self.dict = dict()
    
    def get_pd_orientation(self,player):
      if player==1:return (SCREEN_WIDTH//2,SCREEN_HEIGHT*0.05,0)
      elif player==2:return (SCREEN_WIDTH//2,SCREEN_HEIGHT*0.95,0) if len(self.players) < 3 else (SCREEN_WIDTH*0.05,SCREEN_HEIGHT//2,90)
      elif player==3:return (SCREEN_WIDTH//2,SCREEN_HEIGHT*0.95,0)
      elif player==4:return (SCREEN_WIDTH*0.95,SCREEN_HEIGHT//2,90)


        
    @staticmethod
    def get_tile_orientation(gindex,index,num_players):
      if gindex == 0: return {'image_width':GB_LEN//16,'image_height':GB_LEN//16,'center_x':(SCREEN_WIDTH//2 + PD_HEIGHT*3)-PD_HEIGHT*index,'center_y':SCREEN_HEIGHT*0.05}
      elif gindex ==1 and num_players < 3: return {'image_width':GB_LEN//16,'image_height':GB_LEN//16,'center_x':(SCREEN_WIDTH//2 + PD_HEIGHT*3)-PD_HEIGHT*index,'center_y':SCREEN_HEIGHT*0.95,'angle':180.0}
      elif gindex ==1: return {'image_width':GB_LEN//16,'image_height':GB_LEN//16,'center_x':SCREEN_WIDTH*0.05,'center_y':(SCREEN_HEIGHT//2 + PD_HEIGHT*3)-PD_HEIGHT*index,'angle':270.0}
      elif gindex ==2: return {'image_width':GB_LEN//16,'image_height':GB_LEN//16,'center_x':(SCREEN_WIDTH//2 + PD_HEIGHT*3)-PD_HEIGHT*index,'center_y':SCREEN_HEIGHT*0.95,'angle':180.0}
      elif gindex ==3: return {'image_width':GB_LEN//16,'image_height':GB_LEN//16,'center_x':SCREEN_WIDTH*0.95,'center_y':(SCREEN_HEIGHT//2 + PD_HEIGHT*3)-PD_HEIGHT*index,'angle':90.0}

    def player_create(self,players):
        #self.player_sprites = [arcade.SpriteList(),arcade.SpriteList(),arcade.SpriteList()]
        self.player_sprites = []
        for gindex,player in enumerate(players):
          self.player_sprites.append(arcade.SpriteList())
          for index,char in enumerate(self.Bag.setup()):
            self.player_sprites[gindex].append(Tile(player,char,self.get_tile_orientation(gindex,index,len(players))))
          
        #self.player_sprites = [arcade.SpriteList([Tile(player,char,self.get_orientation(gindex,index,len(players)))for index,char in enumerate(self.Bag.setup())])]
        

      
    def check_slots(self): 
      if self.hand.held.center_x > (SCREEN_WIDTH//2 - GB_LEN//2) and self.hand.held.center_x < (SCREEN_WIDTH//2 + GB_LEN//2) and self.hand.held.center_y > (SCREEN_HEIGHT//2 -GB_LEN//2) and self.hand.held.center_y < (SCREEN_HEIGHT//2 +GB_LEN//2):
          slot_x,slot_y = ((self.hand.held.center_x-(SCREEN_WIDTH//2 - GB_LEN//2))//(GB_LEN//15)),((self.hand.held.center_y-(SCREEN_HEIGHT//2 -GB_LEN//2))//(GB_LEN//15))
          if self.validate_slot(int(slot_x),int(slot_y)):
            self.hand.held.center_x,self.hand.held.center_y = (SCREEN_WIDTH//2 - GB_LEN//2-GB_LEN//30)+(slot_x+1)*(GB_LEN//15),(SCREEN_HEIGHT//2 -GB_LEN//2-GB_LEN//30)+(slot_y+1) *(GB_LEN//15)
            board[int(slot_x)][int(slot_y)] = self.hand.held.letter.name.lower()
            self.hand.selected.add((int(slot_x),int(slot_y))) 
            if self.hand.held_origin.x < (SCREEN_WIDTH//2 - GB_LEN//2) or self.hand.held_origin.x > (SCREEN_WIDTH//2 + GB_LEN//2) or self.hand.held_origin.y < (SCREEN_HEIGHT//2 -GB_LEN//2) or self.hand.held_origin.y > (SCREEN_HEIGHT//2 +GB_LEN//2):
              self.hand.empty_origin.append((self.hand.held_origin.x,self.hand.held_origin.y))
            
            else:
              slot_x,slot_y = ((self.hand.held_origin.x-(SCREEN_WIDTH//2 - GB_LEN//2))//(GB_LEN//15)),((self.hand.held_origin.y-(SCREEN_HEIGHT//2 -GB_LEN//2))//(GB_LEN//15))
              board[int(slot_x)][int(slot_y)] = None
              self.hand.selected.remove((int(slot_x),int(slot_y)))
            
          else: self.hand.held.center_x,self.hand.held.center_y = self.hand.held_origin.x,self.hand.held_origin.y
      elif self.hand.empty_origin:
        i=0
        while i < len(self.hand.empty_origin):
          x,y = self.hand.empty_origin[i][0],self.hand.empty_origin[i][1]
          if self.hand.held.center_x > x-PD_HEIGHT//2 and self.hand.held.center_x < x+PD_HEIGHT//2 and self.hand.held.center_y > y-PD_HEIGHT//2 and self.hand.held.center_y < y+PD_HEIGHT//2:
            if self.hand.held_origin.x < (SCREEN_WIDTH//2 - GB_LEN//2) or self.hand.held_origin.x > (SCREEN_WIDTH//2 + GB_LEN//2) or self.hand.held_origin.y < (SCREEN_HEIGHT//2 -GB_LEN//2) or self.hand.held_origin.y > (SCREEN_HEIGHT//2 +GB_LEN//2):
                self.hand.held.center_x,self.hand.held.center_y = self.hand.empty_origin.pop(i)
                self.hand.empty_origin.append((self.hand.held_origin.x,self.hand.held_origin.y))
          
            else:
              slot_x,slot_y = ((self.hand.held_origin.x-(SCREEN_WIDTH//2 - GB_LEN//2))//(GB_LEN//15)),((self.hand.held_origin.y-(SCREEN_HEIGHT//2 -GB_LEN//2))//(GB_LEN//15))
              board[int(slot_x)][int(slot_y)] = None
              self.hand.selected.remove((int(slot_x),int(slot_y)))
              print(self.hand.selected)
              self.hand.held.center_x,self.hand.held.center_y = self.hand.empty_origin.pop(i)
            return 
          i+= 1
        self.hand.held.center_x,self.hand.held.center_y = self.hand.held_origin.x,self.hand.held_origin.y
          
      else:
        self.hand.held.center_x,self.hand.held.center_y = self.hand.held_origin.x,self.hand.held_origin.y
    
    def validate_slot(self,slot_x,slot_y):
      if board[7][7] is None: return True if slot_x == 7 and slot_y == 7 else False 
      if not board[slot_x][slot_y] is None: return False
      for x,y in ((0,1),(1,0),(0,-1),(-1,0)):
        if slot_x+x >= 0 and slot_x+x < 15 or slot_y+y >= 0 and slot_y+y < 15:
          if not board[slot_x+x][slot_y+y] is None: return True
      return False
      

    def setup(self):
      arcade.set_background_color(arcade.color.RED_DEVIL)
      #arcade.set_viewport(SCREEN_WIDTH//2-CAMERA_WIDTH//2,SCREEN_WIDTH//2+CAMERA_WIDTH//2,SCREEN_HEIGHT//2-CAMERA_HEIGHT//2,SCREEN_HEIGHT//2+CAMERA_HEIGHT//2)
      pass

    
    def on_draw(self):
      arcade.start_render()
      self.draw_game()
      self.manager.draw()
      for i in self.player_sprites:
        i.draw()
      

    def draw_game(self):
      def draw_playerdeck(center_x,center_y,angle):
        arcade.draw_rectangle_filled(center_x,center_y,PD_LENGTH,PD_HEIGHT,(168, 112, 66),tilt_angle=angle)
        arcade.draw_rectangle_outline(center_x,center_y,PD_LENGTH,PD_HEIGHT,(255,255,255), tilt_angle=angle)
        arcade.draw_rectangle_outline(center_x,center_y,PD_LENGTH-(PD_HEIGHT*2),PD_HEIGHT,(255,255,255),tilt_angle=angle)
        arcade.draw_rectangle_outline(center_x,center_y,PD_LENGTH-(PD_HEIGHT*4),PD_HEIGHT,(255,255,255),tilt_angle=angle)
        arcade.draw_rectangle_outline(center_x,center_y,PD_LENGTH-(PD_HEIGHT*6),PD_HEIGHT,(255,255,255),tilt_angle=angle)
          


      arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,GB_LEN, GB_LEN, GB)
      draw_playerdeck(*self.get_pd_orientation(1))
      draw_playerdeck(*self.get_pd_orientation(2)) 
      if len(self.players) >= 3: draw_playerdeck(*self.get_pd_orientation(3))
      if len(self.players) == 4: draw_playerdeck(*self.get_pd_orientation(4))
    
    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, button: int, modifiers: int):
      if button == 1 and not self.hand.held is None:
            self.hand.held.center_x += dx
            self.hand.held.center_y += dy
      elif button == 4:
        a,b,c,d = self.get_viewport()
        self.set_viewport(min(SCREEN_WIDTH//2,max(-(SCREEN_WIDTH//2),a-dx)),min(max(SCREEN_WIDTH//2,b-dx),3*SCREEN_WIDTH//2),min(max(-(SCREEN_HEIGHT//2),c-dy),SCREEN_HEIGHT//2),min(max(SCREEN_HEIGHT//2,d-dy),3*SCREEN_HEIGHT//2))
        self.mouseoffset.x,self.mouseoffset.y = (min(SCREEN_WIDTH//2,max(-(SCREEN_WIDTH//2),a-dx)),min(max(-(SCREEN_HEIGHT//2),c-dy),SCREEN_HEIGHT//2))
    
      pass  

    def on_mouse_scroll(self,x,y,sx,sy):
      #global CAMERA_HEIGHT,CAMERA_WIDTH
      #CAMERA_WIDTH -= sx
      #CAMERA_HEIGHT -= sy

      pass

    
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
      if button == 1:
        tile = arcade.get_sprites_at_point((x+self.mouseoffset.x, y+self.mouseoffset.y), self.player_sprites[self.current_player])
        if len(tile) > 0:
          self.hand.held_origin.x,self.hand.held_origin.y = tile[0].center_x,tile[0].center_y
          self.hand.held = tile[0]
      


    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
      if self.hand.held:
        self.check_slots()
        self.hand.held = None
        self.hand.held_origin.x,self.hand.held_origin.y = 0,0
      pass



    def submit(self):
      #self.hand.extract_words()
      pass



def start():
    make_letters(int(GB_LEN//16)+1)
    window = Display()
    window.setup()
    arcade.run()
