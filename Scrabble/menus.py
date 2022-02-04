from bag import Bag
from board import (
    Board,
    Coords,
    CurrentHand,
    NonLinearWord,
    Slot,
    Word,
    Play
)
from config import *
from cycler import MyCycler
from player import Player
from stats import GameStats, is_connected_to_db,save_stats,make_query

from abc import (
    ABC,
    abstractmethod
)

from copy import deepcopy

from enum import (
    Enum, 
    IntEnum
)
from typing import (
    NamedTuple,
    Optional
)
from threading import Thread
import concurrent.futures
from time import sleep


import arcade
from arcade.gui import (
  UIWidget,
  UIFlatButton,
  UIBoxLayout,
  UILabel,
  UIInputText,
  UIMessageBox,
  UITextArea,
)
from arcade.gui.events import UIMousePressEvent,UITextEvent
from pyglet.event import EVENT_UNHANDLED,EVENT_HANDLED





KEY_C,KEY_P,KEY_S = 99,112,115
ACTIVE,UNACTIVE = True,False

class GameState(IntEnum):
  Title = 0
  Setup = 1
  Setup2 = 2
  Game = 3
  GameFinished = 4
  Settings = 5
  Stats = 6


class UIWidgets(NamedTuple):
    reg_widgets: Optional[list[UIWidget]]
    change_state_buttons: Optional[list[tuple[UIFlatButton,int]]]  
    exit_button: Optional[UIFlatButton] = None


class MyInputText(UIInputText):  

  def __init__(self,**args):
    super().__init__(**args)  
    self.text_entered = False
    self.init_text = ""
    self.layout.selection_color = (50, 151, 253,255)
    self.layout.selection_background_color = (50, 151, 253,200)
    

  def on_event(self, event):

        if not self._active and isinstance(event, UIMousePressEvent):
            if self.rect.collide_with_point(event.x, event.y):
                if self.text_entered == False:
                  self.init_text = self.text
                  self.text = ""
                  self.text_entered = True


        if self._active and isinstance(event, UIMousePressEvent):
            if not self.rect.collide_with_point(event.x, event.y):
                if self.text == "":
                  self.text = self.init_text 
                  self.init_text = ""
                  self.text_entered = False

        
        if self._active:
          if isinstance(event, UITextEvent):
            if len(self.text) == 32:
              return EVENT_UNHANDLED

        if super().on_event(event):
            return EVENT_HANDLED

        return EVENT_UNHANDLED



class Tile(arcade.Sprite):
    def __init__(self,letter:Enum,args):
        super().__init__(filename=f'./Scrabble/tiles/{letter.name}.png',scale=1,**args)
        self.letter = letter




class Menu(ABC):
    background_colour: arcade.color = arcade.color.VIOLET_BLUE#RED_DEVIL
    box_x: str = 'center'
    box_y: str = 'center' 
    state: IntEnum

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def get_ui_widgets(self)-> UIWidgets:
        pass

    
    def on_update(self,delta_time:float):
        pass

    def on_key_press(self, symbol: int, modifiers: int):
        pass

    def on_mouse_scroll(self,x,y,sx,sy):
        pass

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, button: int, modifiers: int):
        return 0

    
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        pass
    
    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        pass

    def get_next_stage_info(self):
        return None
    
    
    def validate(self):
        return 0


class ToBeImplementedMenu(Menu):
    box_x:str = 'center'
    box_y:str = 'center'
    background_colour: arcade.color = arcade.color.DARK_YELLOW

    def draw(self):
        pass

    def get_ui_widgets(self) -> UIWidgets:
        return UIWidgets(reg_widgets=[UILabel(text=f" {self.__class__.__name__} to be Implemented ",font_name=('Open Sans',),font_size=((SCREEN_WIDTH*(4/5))/len(f"{__class__.__name__} to be Implemented")),bold=True,text_color=(0,0,0,255)).with_space_around(bottom=SCREEN_WIDTH//7)],change_state_buttons=[(UIFlatButton(text="Back to Menu", width=SCREEN_WIDTH/3),0)])

class SelectionMenu(Menu):
    box_x: str = 'center'
    box_y: str = 'center' 
    state: IntEnum = GameState(0)

    def draw(self):
        pass


    def get_ui_widgets(self)->UIWidgets:
        scrabble_title = UILabel(text="Scrabble Game",font_name=('Open Sans',),font_size=(SCREEN_WIDTH/19),italic=True,bold=True)
        scrabble_title = scrabble_title.with_space_around(bottom=SCREEN_HEIGHT//7)

        start_button = UIFlatButton(text="Play Game", width=SCREEN_WIDTH//5)
        

        settings_button = UIFlatButton(text="Settings", width=SCREEN_WIDTH//5)
        
        
        stat_button = UIFlatButton(text="Stats", width=SCREEN_WIDTH//5)
    

        exit_button =  UIFlatButton(text="Exit", width=SCREEN_WIDTH//5)
        
        
        return UIWidgets(reg_widgets=[scrabble_title],change_state_buttons=[(start_button,1),(settings_button,5),(stat_button,6)],exit_button=exit_button)
        


    
class SetupMenu1(Menu):
    box_x: str = 'center'
    box_y: str = 'top'
    state: IntEnum = GameState(1)
    background_colour: arcade.color = arcade.color.AMAZON


    def __init__(self):
        self.player_count: int = 2
        self.points_to_win:int = 100
        self.word_stats:bool = True
        self.action_stats:bool = True

   
    def draw(self):
        pass

    def get_ui_widgets(self) -> UIWidgets:
        
        #Number of players 
        #only top center for now if more options top left
        top_left = UIBoxLayout()
        top_left.add(UILabel(text="Num of Players",font_name=('Open Sans',),font_size=(SCREEN_WIDTH/60),bold=True))

        count_lbl = UILabel(text="   2   ",font_name=('Open Sans',),font_size=(SCREEN_WIDTH/50),bold=True)

        self.player_count = count_lbl.text

        top_left.add(count_lbl)
        
        top_left_bottom = UIBoxLayout(vertical=False)
        add_btn = UIFlatButton(text=" + ", width=SCREEN_WIDTH//10)
        sub_btn = UIFlatButton(text=" - ", width=SCREEN_WIDTH//10)

        def add1():
            count_lbl.text = ("   "+str(int(count_lbl.text)+1)+"   ") if int(count_lbl.text) < 4 else "   4   "
            self.player_count = count_lbl.text
        def sub1():
            count_lbl.text = ("   "+str(int(count_lbl.text)-1)+"   ") if int(count_lbl.text) > 2 else "   2   "
            self.player_count = count_lbl.text

        add_btn.on_click = lambda event:add1()
        sub_btn.on_click = lambda event:sub1()

        top_left_bottom.add(add_btn)
        top_left_bottom.add(sub_btn)

        top_left.add(top_left_bottom)





        top_middle = UIBoxLayout()
        top_middle.add(UILabel(text="Points to Win Game",font_name=('Open Sans',),font_size=(SCREEN_WIDTH/60),bold=True))
        count_lbl2 = UILabel(text="   100   ",font_name=('Open Sans',),font_size =SCREEN_WIDTH//50,bold=True)
        self.points_to_win = count_lbl2.text 
        top_middle.add(count_lbl2)
        top_middle_bottom = UIBoxLayout(vertical=False)
        add2_btn = UIFlatButton(text=" + ", width=SCREEN_WIDTH//10)
        sub2_btn = UIFlatButton(text=" - ", width=SCREEN_WIDTH//10)

        def add2():
            count_lbl2.text = ("   "+str(int(count_lbl2.text)+25)+"   ") if int(count_lbl2.text) < 200 else "   200   "
            self.points_to_win = count_lbl2.text
        def sub2():
            count_lbl2.text = ("   "+str(int(count_lbl2.text)-25)+"   ") if int(count_lbl2.text) > 50 else "   50   "
            self.points_to_win = count_lbl2.text

        add2_btn.on_click = lambda event:add2()
        sub2_btn.on_click = lambda event:sub2()

        top_middle_bottom.add(add2_btn)
        top_middle_bottom.add(sub2_btn)

        top_middle.add(top_middle_bottom)
        top_middle.with_space_around(left=SCREEN_WIDTH/7,right=SCREEN_WIDTH/7)


        top_right = UIBoxLayout()
        top_right.add(UILabel(text="Stats to Save?",font_name=('Open Sans',),font_size=(SCREEN_WIDTH/60),bold=True))
        
        word_lbl =  UILabel(text=" Words:Yes ",font_name=('Open Sans',),font_size =SCREEN_WIDTH//75,bold=True)
        action_lbl = UILabel(text=" Actions:Yes ",font_name=('Open Sans',),font_size =SCREEN_WIDTH//75,bold=True)

        def word_change():
            word_lbl.text = " Words:No " if self.word_stats else  " Words:Yes "
            self.word_stats = not self.word_stats
        
        def action_change():
            action_lbl.text = " Actions:No " if self.action_stats else  " Actions:Yes "
            self.action_stats = not self.action_stats

        
        word_btn = UIFlatButton(text=" x ", width=SCREEN_WIDTH//10)
        action_btn = UIFlatButton(text=" x ", width=SCREEN_WIDTH//10)
        word_btn.on_click = lambda event: word_change()
        action_btn.on_click = lambda event: action_change()

        top_right_horizontal = UIBoxLayout(vertical=False)
        top_right_left = UIBoxLayout()
        top_right_right = UIBoxLayout()
       


        top_right_left.add(word_lbl)
        top_right_right.add(action_lbl)
        top_right_left.add(word_btn)
        top_right_right.add(action_btn)


        top_right_horizontal.add(top_right_left)
        top_right_horizontal.add(top_right_right)
        top_right.add(top_right_horizontal.with_space_around(top=SCREEN_HEIGHT/50))
        

        top = UIBoxLayout(vertical=False)
        top.add(top_left)
        top.add(top_middle)
        top.add(top_right)
        top = top.with_space_around(bottom=SCREEN_HEIGHT/10)

        next_btn = UIFlatButton(text="Next >", width=SCREEN_WIDTH//5)
        

        return UIWidgets(reg_widgets=[top],change_state_buttons=[(next_btn,2)])
    

    def get_next_stage_info(self):
        return (int([value for value in self.player_count if value != " "][0]),int([value for value in self.points_to_win if value != " "][0]),self.word_stats,self.action_stats)


class SetupMenu2(Menu):
    box_x: str = 'center'
    box_y: str = 'top'
    state: IntEnum = GameState(2)
    background_colour: arcade.color = arcade.color.AMAZON


    def __init__(self,numberofplayers:int,*extra_info):
        self.num_of_players:int = numberofplayers
        self.player_names:list[str] = []
        self.extra_info = extra_info
        

    def draw(self):
        pass

    def get_ui_widgets(self) -> UIWidgets:
        rows = []
        row = UIBoxLayout(vertical=False)
        for i in range(self.num_of_players):
            if i%2 == 0:
                rows.append(UIBoxLayout(vertical=False))
            box = UIBoxLayout()
            name_label = UILabel(text=f"        Player{i+1}'s Name       ",font_name=('Open Sans',),font_size=(SCREEN_WIDTH/50),bold=True,width=SCREEN_WIDTH//3,text_color=arcade.color.WHITE)
            box.add(name_label)
            name_input = MyInputText(text='      Enter an alphebetical Name      ',font_size=(SCREEN_WIDTH/75),font_name=('Open Sans',),width=SCREEN_WIDTH//3,height=50)
            self.player_names.append(name_input)
            name_input = name_input.with_space_around(bg_color=arcade.color.WHITE)
            box.add(name_input)
            rows[-1].add(box.with_space_around(left=SCREEN_WIDTH//10,bottom=SCREEN_WIDTH//10) if i%2 == 1 else box.with_space_around(bottom=SCREEN_WIDTH//10))
            
            
        names_button = UIFlatButton(text="Start Game", width=SCREEN_WIDTH//5)

        return UIWidgets(reg_widgets=rows,change_state_buttons=[(names_button,3)])
    
    def validate(self):
        for i in self.player_names:
            if i.text == "" or i.text == 'Enter an Alphebetical Name' or not i.text.isalpha():
                return 1 
        if len(self.player_names) != len(set(i.text for i in self.player_names)): return 1
        return 0 

    def get_next_stage_info(self):
        return (self.extra_info[0],self.extra_info[1],self.extra_info[2],[i.text for i in self.player_names])
        #return [Player(self.player_names[j].text,self.create_sprite_list(j,len(self.player_names))) for j in range(len(self.player_names))]


class GameMenu(Menu):
    box_x:str = 'center'
    box_y:str = 'center'
    state:IntEnum = GameState(3)
    background_colour: arcade.color = arcade.color.RED_DEVIL

  

    def __init__(self,points_to_win:int,if_word_stats:bool,if_action_stats:bool,players:list[str]):
        self.bag:Bag = Bag(1 if len(players) != 4 else 2)
        self.board:Board = Board()  
        self.hand:CurrentHand = CurrentHand()
        self.screenoffset:Coords = Coords()
        self.points_to_win:int = points_to_win
        

        self.players:list[Player] = [Player(players[j],self.create_sprite_list(j,len(players))) for j in range(len(players))] 
        self.cycler:MyCycler =  MyCycler(self.players)
        self.current_player:int = self.cycler.get_first_player(self.players)

        self.center:UIBoxLayout = UIBoxLayout()
    
        self.placed:list[tuple[float,float,float,float]] = []
        self.tiles_to_shuffle:list[Tile] = []
        self.words:Play = None


        self.s:bool = ACTIVE
        self.p:bool = ACTIVE
        self.c:bool = UNACTIVE
        self.error:bool = UNACTIVE
        self.challenging :bool = UNACTIVE
        self.shuffling: bool = UNACTIVE
        self.move_freeze:bool = UNACTIVE

        self.event_center:bool = ACTIVE
        self.event_reset:bool = False
        self.event_end_game:bool = False
        if is_connected_to_db():
            self.game_stats:GameStats = GameStats(self.players)
        else:
            def set_controls_back(_):
                self.p = self.s = ACTIVE
                self.move_freeze = UNACTIVE

            self.game_stats = None
            self.p = self.s = UNACTIVE
            self.move_freeze = ACTIVE
            self.center.add(UIMessageBox(width=SCREEN_WIDTH/2.25,height=SCREEN_HEIGHT/2.25,message_text=f'Connection to DB failed. Stats will not be Saved',callback=set_controls_back))
        
        self.word_stats:bool = if_word_stats
        self.action_stats:bool = if_action_stats


    def draw(self)->None:
      self.draw_gameboard()

      self.draw_playerdeck(*self.get_pd_orientation(0,len(self.players)))
      self.draw_playerdeck(*self.get_pd_orientation(1,len(self.players))) 
      if len(self.players) >= 3: self.draw_playerdeck(*self.get_pd_orientation(2,len(self.players)))
      if len(self.players) == 4: self.draw_playerdeck(*self.get_pd_orientation(3,len(self.players)))

      self.draw_sprites()

      if self.placed: self.draw_outline_of_chains()
      self.draw_placed_tile_outline()

      if self.shuffling:arcade.draw_text(f"Shuffeling mode is on!",0+self.screenoffset.x,SCREEN_HEIGHT*(9/10)+self.screenoffset.y,(255,255,255),font_size=SCREEN_WIDTH//30,font_name=('Open Sans',),bold=True,rotation=0)
        
    def get_ui_widgets(self) -> UIWidgets:
        return UIWidgets(reg_widgets=[self.center],change_state_buttons=[])
        pass 


    def get_next_stage_info(self)->tuple[str,int]:
        return (self.players[self.current_player].name,self.players[self.current_player].points)

    def on_update(self,delta_time:float):
        if self.challenging  is False and self.event_reset is True: 
            self.event_reset = False
            if self.words is None: return 
            temp = self.words
            self.words = None
            self.c = UNACTIVE
            text = f"{self.players[self.current_player].name} has scored: {temp.get_points()} Points\n\nPlayer main word: {temp.main_word}={temp.main_word.value*temp.main_word.word_amp}P \n\nPlayer chain words:\n     "+"".join([f'{i}={i.value*i.word_amp}P,\n     ' for i in temp.chains])
            self.center.add(UIMessageBox(width=SCREEN_WIDTH/2.25,height=SCREEN_HEIGHT/2.25,message_text=text,callback=lambda text: self.progress_game(temp)))
            self.event_center = ACTIVE
        elif self.event_center:
            self.event_center = UNACTIVE
            self.screenoffset.x,self.screenoffset.y = 0,0
            return ('center',) 
        elif self.event_end_game is True: 
            if not self.game_stats is None: save_stats(self.game_stats,self.word_stats,self.action_stats)
            return ('change_state',4,self.get_next_stage_info())
            

    

    def on_key_press(self, symbol: int, modifiers: int)->None:
        if self.p is ACTIVE and symbol == KEY_P:
            self.finalize_play()  
            if not self.game_stats is None: self.game_stats.num_of_plays += 1
        if self.s is ACTIVE and symbol == KEY_S:
            self.shuffle()
            if not self.game_stats is None:self.game_stats.num_of_shuffles += 1
        elif self.c is ACTIVE and symbol == KEY_C: 
            self.challenge()
            if not self.game_stats is None: self.game_stats.num_of_challenges += 1
            pass

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, button: int, modifiers: int)->int:
        if self.move_freeze is ACTIVE: return
        if button == 1 and not self.hand.held is None:
              self.hand.held.center_x += dx
              self.hand.held.center_y += dy
        return 1

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int)->None:
        if self.move_freeze is ACTIVE: return
        if button == 1:
            tile = arcade.get_sprites_at_point((x+self.screenoffset.x, y+self.screenoffset.y), self.players[self.current_player].sprites)
            if len(tile) > 0:

                if not self.shuffling:
                    self.hand.held_origin.x,self.hand.held_origin.y = tile[0].center_x,tile[0].center_y
                    self.hand.held = tile[0]
                else:
                    if tile[0] not in self.tiles_to_shuffle:
                        self.tiles_to_shuffle.append(tile[0])
                    else:
                        self.tiles_to_shuffle.remove(tile[0])
    
    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int)->None:
        if self.move_freeze is ACTIVE: return
        if button ==1 and self.hand.held:
            self.check_released_slot()
            self.hand.held = None
            self.hand.held_origin.x,self.hand.held_origin.y = 0,0


    
    def finalize_play(self)->None:
        if len(self.hand.selected) < 2: return 
        if self.hand.held:
            self.hand.held.center_x,self.hand.held.center_y = self.hand.held_origin.x,self.hand.held_origin.y
            self.hand.held = None
            self.hand.held_origin = None
        try: 
            words = self.board.evaluate_play(deepcopy(self.hand.selected))
        except NonLinearWord:
            t = Thread(target=self.WordIsNotLinear)
            t.start()
            return 
  
        t = Thread(target=lambda :self.create_placed_indicator(words))
        t.start()


    def shuffle(self)-> None:
        def set_controls_back(_):
            self.p = self.s = ACTIVE
            self.move_freeze = UNACTIVE


        if self.shuffling == UNACTIVE:
            self.shuffling = ACTIVE
            self.p = UNACTIVE
        else:
            if self.tiles_to_shuffle:
                self.s = ACTIVE
                self.move_freeze = UNACTIVE
                self.event_center = ACTIVE
                

                self.bag.extend_bag([i.letter for i in self.tiles_to_shuffle])
                while self.tiles_to_shuffle: 
                    temp = self.tiles_to_shuffle.pop()
                    new_tile = self.make_sprite(Coords(temp.center_x,temp.center_y) if not self.on_gameboard(temp.center_x,temp.center_y) else self.hand.empty_origin.pop())
                    self.players[self.current_player].sprites.pop(self.players[self.current_player].sprites.index(temp))
                    self.players[self.current_player].sprites.append(new_tile)
                

                self.shuffling = UNACTIVE

                self.clean_gameboard()
                self.current_player = self.cycler.next_player()

                self.center.add(UIMessageBox(width=SCREEN_WIDTH/2.25,height=SCREEN_HEIGHT/2.25,message_text=f'Turn has ended! Next Player is {self.players[self.current_player].name}',callback=set_controls_back))
                
                

            else:
                self.shuffling = UNACTIVE
                self.p = ACTIVE


    def challenge(self)->None:
        self.challenging  = ACTIVE
        self.c = UNACTIVE
        self.event_center = ACTIVE

        header = UILabel(width=SCREEN_WIDTH*(1/3),height=SCREEN_HEIGHT//15,text=f"Please select  challenger's name",font_name=('Open Sans',),font_size=(SCREEN_WIDTH*(2/3))/32,bold=True).with_space_around(bg_color=arcade.color.BLACK)
        row1 = UIBoxLayout(vertical=False)
        row2 = UIBoxLayout(vertical=False)
        

        button1 = UIFlatButton(width=SCREEN_WIDTH*(1/6),height=SCREEN_HEIGHT*(1/6),text=self.players[0].name,font_name=('Open Sans',),font_size=(SCREEN_WIDTH*(1/3))/len(self.players[0].name),style={'bg_color':(10, 204, 126),'border_color':(255,255,255)})
        button2 = UIFlatButton(width=SCREEN_WIDTH*(1/6),height=SCREEN_HEIGHT*(1/6),text=self.players[1].name,font_name=('Open Sans',),font_size=(SCREEN_WIDTH*(1/3))/len(self.players[1].name),style={'bg_color':(50, 24, 217),'border_color':(255,255,255)})

        button1.on_click = lambda event: self.validate_words(0) 
        button2.on_click = lambda event: self.validate_words(1)
        row1.add(button1)
        row1.add(button2)

        if len(self.players) > 2: 
            button3 = UIFlatButton(width=SCREEN_WIDTH*(1/6),height=SCREEN_HEIGHT*(1/6),text=self.players[2].name,font_name=('Open Sans',),font_size=(SCREEN_WIDTH*(1/3))/len(self.players[2].name),style={'bg_color':(212, 4, 25),'border_color':(255,255,255)})
            button3.on_click = lambda event: self.validate_words(2)
            row2.add(button3)
            if len(self.players) > 3: 
                button4 = UIFlatButton(width=SCREEN_WIDTH*(1/6),height=SCREEN_HEIGHT*(1/6),text=self.players[3].name,font_name=('Open Sans',),font_size=(SCREEN_WIDTH*(1/3))/len(self.players[3].name),style={'bg_color':(242, 235, 12),'border_color':(255,255,255)})
                button4.on_click = lambda event: self.validate_words(3)
                row2.add(button4)

        row1 = row1.with_space_around(bg_color=arcade.color.WHITE)
        row2 = row2.with_space_around(bg_color=arcade.color.WHITE)
        footer = UIFlatButton(width=SCREEN_WIDTH*(1/3),height=SCREEN_HEIGHT//15,text="Cancel Challenge")
        def resume_play():
            self.center.clear() 
            self.challenging  = UNACTIVE
        footer.on_click = lambda event: resume_play()
        self.center.add(header)
        self.center.add(row1)
        self.center.add(row2)
        self.center.add(footer)

    def validate_words(self,challenger:int):
        self.center.clear()
        list_of_words = [str(i).lower() for i in self.words.chains] + [str(self.words.main_word).lower()]
        result_container = ([],[])
        with concurrent.futures.ThreadPoolExecutor() as executor: 
            results = executor.map(self.board.word_checker.check,list_of_words)

            for result in results:
                if result[0] is False: result_container[0].append(result[1])
                else: result_container[1].append((result[1],result[2]))

        was_correct = True if result_container[0] else False
        text = 'WORDS NOT IN DICTIONARY:\n\n' + ''.join(["     -"+i.capitalize()+"\n" for i in result_container[0]]) + '\nWORDS IN DICTIONARY:\n\n' + "".join([i[0].capitalize()+'='+str(i[1] if not i[1] is None else 'N/A')+'\n\n' for i in result_container[1]]) + '\n\n\n\n\n'
        self.center.add(UITextArea(width=(SCREEN_WIDTH*(2/3)),height=(SCREEN_HEIGHT*(2/3)),text=text,font_name=('Open Sans',),text_color=arcade.color.RED_DEVIL).with_space_around(bg_color=arcade.color.WHITE))
        button = UIFlatButton(text='Finished',width=(SCREEN_WIDTH*(2/3)),height=(SCREEN_HEIGHT//10))
        button.on_click = lambda event: self.center.clear() or self.center.add(UIMessageBox(width=SCREEN_WIDTH/2.25,height=SCREEN_HEIGHT/2.25,message_text=f"{self.players[challenger].name} was CORRECT. {self.players[self.current_player].name}'s play will be REVOKED" if was_correct else f"{self.players[challenger].name} was INCORRECt. {self.players[challenger].name}'s next move will be skipped",callback= lambda text:self.finish_challenge(challenger,was_correct)))
        self.center.add(button) 
            
    def finish_challenge(self,challenger:int,was_correct:bool)->None:
        def set_controls_back(_):
            self.p = self.s = ACTIVE
            self.move_freeze = UNACTIVE

        if was_correct is True:
            self.clean_gameboard()
            self.current_player = self.cycler.next_player()
            self.center.add(UIMessageBox(width=SCREEN_WIDTH/2.25,height=SCREEN_HEIGHT/2.25,message_text=f'Turn has ended! Next Player is {self.players[self.current_player].name}',callback=set_controls_back))
            
            self.board.clean_word_map_of_invalid_play(self.words)
            self.event_reset = False
            self.words = None
            self.challenging  = UNACTIVE
            
            
        else:
            self.cycler.add_to_blacklist(challenger)
            self.challenging  = UNACTIVE




    def clean_gameboard(self):
            i = 0
            while i < len(self.players[self.current_player].sprites):
                if self.on_gameboard(self.players[self.current_player].sprites[i].center_x,self.players[self.current_player].sprites[i].center_y):
                    origin = self.hand.empty_origin.pop()
                    self.players[self.current_player].sprites[i].center_x,self.players[self.current_player].sprites[i].center_y = origin.x,origin.y
                else:
                    i+=1 
            while self.hand.selected:
                temp = self.hand.selected.pop()
                self.board.place_on_board(temp.col,temp.row,None) 
            



    def check_released_slot(self)->None:
        if self.on_gameboard(self.hand.held.center_x,self.hand.held.center_y):
            col,row = self.get_gameboard_slots(self.hand.held.center_x,self.hand.held.center_y)

            if self.board.slot_used(col,row):
                gb_tile = arcade.get_sprites_at_point(self.get_coords_of_slot(col,row),self.players[self.current_player].sprites) #list
                if len(gb_tile) <= 1: 
                    self.hand.held.center_x,self.hand.held.center_y = self.hand.held_origin.x,self.hand.held_origin.y
                    return
                else: gb_tile = gb_tile[0] if gb_tile[0] != self.hand.held else gb_tile[1]

                if not self.on_gameboard(self.hand.held_origin.x,self.hand.held_origin.y):
                    self.board.place_on_board(col,row,self.hand.held.letter)
                    self.swap_positions_and_angles_with_held(self.hand.held,self.hand.held_origin,gb_tile)
                    return 

                else:
                    moved_obj_prev_col,moved_obj_prev_row = self.get_gameboard_slots(self.hand.held_origin.x,self.hand.held_origin.y)
                    self.board.swap_on_board(col,row,moved_obj_prev_col,moved_obj_prev_row)
                    self.swap_positions_and_angles_with_held(self.hand.held,self.hand.held_origin,gb_tile)
                    return 
    
            elif self.board.validate_slot(col,row,self.validate_displacement(self.on_gameboard(self.hand.held_origin.x,self.hand.held_origin.y))):
                self.hand.held.center_x,self.hand.held.center_y = self.get_coords_of_slot(col,row)
                self.board.place_on_board(col,row,self.hand.held.letter)
                self.hand.held.angle = 0
                self.hand.selected.add(Slot(col,row))
                
                
                if not self.on_gameboard(self.hand.held_origin.x,self.hand.held_origin.y):
                    self.hand.empty_origin.append(Coords(self.hand.held_origin.x,self.hand.held_origin.y))
                else:
                    prev_col,prev_row = self.get_gameboard_slots(self.hand.held_origin.x,self.hand.held_origin.y)
                    self.board.place_on_board(prev_col,prev_row,None)
                    self.hand.selected.remove((prev_col,prev_row))
            
            

            else: self.hand.held.center_x,self.hand.held.center_y = self.hand.held_origin.x,self.hand.held_origin.y
        


        elif len(pd_tile := arcade.get_sprites_at_point((self.hand.held.center_x,self.hand.held.center_y),self.players[self.current_player].sprites)) > 1:
            pd_tile = pd_tile = pd_tile[0] if pd_tile[0] != self.hand.held else pd_tile[1]
            if not self.on_gameboard(self.hand.held_origin.x,self.hand.held_origin.y):
                self.swap_positions_and_angles_with_held(self.hand.held,self.hand.held_origin,pd_tile)
            else:
                prev_col,prev_row = self.get_gameboard_slots(self.hand.held_origin.x,self.hand.held_origin.y)
                self.board.place_on_board(prev_col,prev_row,pd_tile.letter)
                self.swap_positions_and_angles_with_held(self.hand.held,self.hand.held_origin,pd_tile)


        elif self.hand.empty_origin:
            i=0
            while i < len(self.hand.empty_origin):
            
                x,y = self.hand.empty_origin[i].x,self.hand.empty_origin[i].y
                if self.on_playerdeck(self.hand.held.center_x,self.hand.held.center_y,x,y):
                    if not self.on_gameboard(self.hand.held_origin.x,self.hand.held_origin.y):
                        pd_slot = self.hand.empty_origin.pop(i)
                        self.hand.held.center_x,self.hand.held.center_y = pd_slot.x,pd_slot.y
                        self.hand.empty_origin.append((self.hand.held_origin.x,self.hand.held_origin.y))
                    
                    else:
                        prev_col,prev_row = self.get_gameboard_slots(self.hand.held_origin.x,self.hand.held_origin.y)
                        self.board.place_on_board(prev_col,prev_row,None)
                        self.hand.selected.remove((prev_col,prev_row))
                        pd_slot = self.hand.empty_origin.pop(i)
                        self.hand.held.center_x,self.hand.held.center_y = pd_slot.x,pd_slot.y
                        self.hand.held.angle = self.get_tilt_angle(self.current_player,len(self.players))
        

                    return 
                i+= 1
            self.hand.held.center_x,self.hand.held.center_y = self.hand.held_origin.x,self.hand.held_origin.y
          
        else:
            self.hand.held.center_x,self.hand.held.center_y = self.hand.held_origin.x,self.hand.held_origin.y




    def create_sprite_list(self,pindex,numofplayers)->list[Tile]:
        tiles = arcade.SpriteList()
        for index,char in enumerate(self.bag.player_setup()):
          tiles.append(Tile(char,self.get_tile_orientation(pindex,index,numofplayers)))
        return tiles

    
    def draw_gameboard(self)->None:
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,GB_LEN, GB_LEN, GB)

    def draw_playerdeck(self,player,center_x,center_y,angle,text_center_x,text_center_y)->None:
        arcade.draw_rectangle_filled(center_x,center_y,PD_LENGTH,PD_HEIGHT,(168, 112, 66),tilt_angle=angle)
        arcade.draw_rectangle_outline(center_x,center_y,PD_LENGTH,PD_HEIGHT,(255,255,255), tilt_angle=angle)
        arcade.draw_rectangle_outline(center_x,center_y,PD_LENGTH-(PD_HEIGHT*2),PD_HEIGHT,(255,255,255),tilt_angle=angle)
        arcade.draw_rectangle_outline(center_x,center_y,PD_LENGTH-(PD_HEIGHT*4),PD_HEIGHT,(255,255,255),tilt_angle=angle)
        arcade.draw_rectangle_outline(center_x,center_y,PD_LENGTH-(PD_HEIGHT*6),PD_HEIGHT,(255,255,255),tilt_angle=angle)
        arcade.draw_text(f"{self.players[player].name}:{self.players[player].points}",text_center_x,text_center_y,(255,255,255) if player != self.current_player else (57, 255, 20),font_size=SCREEN_HEIGHT//45,font_name=('Open Sans',),bold=True,rotation=angle)

    def draw_sprites(self)->None:
        self.board.board_tiles.draw()
        self.players[self.current_player].sprites.draw()

    def draw_placed_tile_outline(self)->None:
        for i in self.players[self.current_player].sprites:
            if i != self.hand.held:
                if i.center_x > (SCREEN_WIDTH//2 - GB_LEN//2) and i.center_x < (SCREEN_WIDTH//2 + GB_LEN//2) and i.center_y > (SCREEN_HEIGHT//2 -GB_LEN//2) and i.center_y < (SCREEN_HEIGHT//2 +GB_LEN//2):
                    arcade.draw_rectangle_outline(i.center_x,i.center_y,PD_HEIGHT,PD_HEIGHT,(57, 255, 20) if self.error is UNACTIVE else (255, 0, 0),border_width=2,tilt_angle=0)

        for i in self.tiles_to_shuffle:
            arcade.draw_rectangle_outline(i.center_x,i.center_y,PD_HEIGHT,PD_HEIGHT,(217, 255, 0),border_width=2,tilt_angle=0)


    def draw_outline_of_chains(self)->None:
        for i in self.placed: arcade.draw_rectangle_outline(*i,(0, 255, 247),2)



    def on_gameboard(self,x:float,y:float) -> bool:
        return x > (SCREEN_WIDTH//2 - GB_LEN//2) and x < (SCREEN_WIDTH//2 + GB_LEN//2) and y > (SCREEN_HEIGHT//2 -GB_LEN//2) and y < (SCREEN_HEIGHT//2 +GB_LEN//2)

    def get_gameboard_slots(self,x:float,y:float) -> tuple[int,int]:
        return int((x-(SCREEN_WIDTH//2 - GB_LEN//2))//(GB_LEN//15)),int((y-(SCREEN_HEIGHT//2 -GB_LEN//2))//(GB_LEN//15))

    def get_coords_of_slot(self,col,row)->tuple[float,float]:
        return (SCREEN_WIDTH/2 - GB_LEN/2-GB_LEN/30)+(col+1)*(GB_LEN/15),(SCREEN_HEIGHT/2 -GB_LEN/2-GB_LEN/30)+(row+1) *(GB_LEN/15)
    
    #Check if the the tile is not beside itself on  the gameboard
    def validate_displacement(self,on_gameboard=True)->bool:
        if on_gameboard is True:
            x,y = (abs(self.hand.held_origin.x-self.hand.held.center_x)),(abs(self.hand.held_origin.y-self.hand.held.center_y)) 
            if x > PD_HEIGHT*(3/2) or y > PD_HEIGHT*(3/2): return False 
            return True if (x > PD_HEIGHT/2 and x < (PD_HEIGHT*(3/2))) ^ (y > PD_HEIGHT/2 and y < (PD_HEIGHT*(3/2))) else False 
        else: return False
     
    def on_playerdeck(self,x:float,y:float,pdsx:float,pdsy:float):
        #pdsx,pdsy refers to a player deck slot x and y center coords
        return x > pdsx-PD_HEIGHT//2 and x < pdsx+PD_HEIGHT//2 and y > pdsy-PD_HEIGHT//2 and y < pdsy+PD_HEIGHT//2

    def WordIsNotLinear(self):
        self.error = ACTIVE
        self.p = self.s = UNACTIVE
        sleep(3.5)
        self.error = UNACTIVE
        self.p = self.s = ACTIVE


    

    def create_placed_gridline(self,words:list[tuple[Slot,Slot]]) -> list[tuple[float,float,float,float]]:
        arr = []
        for i in words:
            if i[0].col == i[1].col:
                center_x,center_y = self.get_coords_of_slot(i[0].col,(i[0].row+i[1].row)/2)
                height = (i[1].row-i[0].row+1)*(PD_HEIGHT)
                arr.append((center_x,center_y,PD_HEIGHT,height))
            else:
                center_x,center_y = self.get_coords_of_slot((i[0].col+i[1].col)/2,i[0].row)
                width = (i[1].col - i[0].col+1)*(PD_HEIGHT)
                arr.append((center_x,center_y,width,PD_HEIGHT))
        return arr

    def create_placed_indicator(self,words:Play)->None:
        self.move_freeze = ACTIVE
        self.p = self.s = UNACTIVE
        self.c = ACTIVE
        self.placed = self.create_placed_gridline(([(i.beg,i.end) for i in words.chains]+[(words.main_word.beg,words.main_word.end)]))
        self.words = words
        sleep(7)
        self.placed.clear()
        self.event_reset = True 



    def make_sprite(self,origin:Coords)-> Tile:
        return Tile(self.bag.grab_next(),{'image_width':GB_LEN//16,'image_height':GB_LEN//16,'center_x':origin.x,'center_y':origin.y,'angle':self.get_tilt_angle(self.current_player,len(self.players))})

    def reset_play(self)->None:
        self.hand.selected.clear()
        board_tiles = arcade.SpriteList()
        i = 0
        while i < len(self.players[self.current_player].sprites):
            if self.on_gameboard(self.players[self.current_player].sprites[i].center_x,self.players[self.current_player].sprites[i].center_y):
                board_tiles.append(self.players[self.current_player].sprites.pop(i))
            else:
                i+=1 
        self.board.add_tiles(board_tiles)
        while self.hand.empty_origin:
            self.players[self.current_player].sprites.append(self.make_sprite(self.hand.empty_origin.pop()))

    def progress_game(self,words:Play)-> None:
        def set_controls_back(_):
            self.p = self.s = ACTIVE
            self.move_freeze = UNACTIVE

        self.reset_play()
        self.players[self.current_player].points += words.get_points()
        self.players[self.current_player].words.append(words)

        if self.players[self.current_player].points >= self.points_to_win: 
            self.event_end_game = True
            return

        self.current_player = self.cycler.next_player()
        self.center.add(UIMessageBox(width=SCREEN_WIDTH/2.25,height=SCREEN_HEIGHT/2.25,message_text=f'Turn has ended! Next Player is {self.players[self.current_player].name}',callback=set_controls_back))


    
    @staticmethod
    def get_tilt_angle(current_player:int,numofplayers:int) -> int:
        if current_player == 0: return 0
        elif current_player == 1: return 180 if numofplayers  < 3 else 90
        elif current_player == 2: return 180
        else: return 270

    @staticmethod
    def swap_positions_and_angles_with_held(t1:Tile,origin:Coords,t2:Tile)->None:
        t1.center_x,t1.center_y = t2.center_x,t2.center_y
        t2.center_x,t2.center_y = origin.x,origin.y
        t1.angle,t2.angle = t2.angle,t1.angle

    @staticmethod
    def get_tile_orientation(gindex,index,num_players)->None:
      if gindex == 0: return {'image_width':GB_LEN//16,'image_height':GB_LEN//16,'center_x':(SCREEN_WIDTH//2 + PD_HEIGHT*3)-PD_HEIGHT*index,'center_y':SCREEN_HEIGHT*0.05}
      elif gindex ==1 and num_players < 3: return {'image_width':GB_LEN//16,'image_height':GB_LEN//16,'center_x':(SCREEN_WIDTH//2 + PD_HEIGHT*3)-PD_HEIGHT*index,'center_y':SCREEN_HEIGHT*0.95,'angle':180.0}
      elif gindex ==1: return {'image_width':GB_LEN//16,'image_height':GB_LEN//16,'center_x':SCREEN_WIDTH*0.05,'center_y':(SCREEN_HEIGHT//2 + PD_HEIGHT*3)-PD_HEIGHT*index,'angle':270.0}
      elif gindex ==2: return {'image_width':GB_LEN//16,'image_height':GB_LEN//16,'center_x':(SCREEN_WIDTH//2 + PD_HEIGHT*3)-PD_HEIGHT*index,'center_y':SCREEN_HEIGHT*0.95,'angle':180.0}
      elif gindex ==3: return {'image_width':GB_LEN//16,'image_height':GB_LEN//16,'center_x':SCREEN_WIDTH*0.95,'center_y':(SCREEN_HEIGHT//2 + PD_HEIGHT*3)-PD_HEIGHT*index,'angle':90.0}

    #Dimensions to create player_deck
    @staticmethod
    def get_pd_orientation(player,numofplayers)->None:
      if player==0:return (player,SCREEN_WIDTH//2,SCREEN_HEIGHT*0.05,0,SCREEN_WIDTH//2-(PD_LENGTH/2),(SCREEN_HEIGHT*0.05)+GB_LEN/25)
      elif player==1:return (player,SCREEN_WIDTH//2,SCREEN_HEIGHT*0.95,180,SCREEN_WIDTH//2+(PD_LENGTH/2),(SCREEN_HEIGHT*0.95)-GB_LEN/25) if numofplayers < 3 else (player,SCREEN_WIDTH*0.05,SCREEN_HEIGHT//2,270,(SCREEN_WIDTH*0.05)+GB_LEN//25,SCREEN_HEIGHT//2+(PD_LENGTH/2))
      elif player==2:return (player,SCREEN_WIDTH//2,SCREEN_HEIGHT*0.95,180,SCREEN_WIDTH//2+(PD_LENGTH/2),(SCREEN_HEIGHT*0.95)-GB_LEN/25)
      elif player==3:return (player,SCREEN_WIDTH*0.95,SCREEN_HEIGHT//2,90,(SCREEN_WIDTH*0.95)-GB_LEN/25,SCREEN_HEIGHT//2-(PD_LENGTH/2))


        
class GameFinishedMenu(Menu):
    box_x:str = 'center'
    box_y:str = 'center'
    state:IntEnum = GameState(4)
    background_colour: arcade.color = arcade.color.CYAN

    def __init__(self,player_name,player_points):
        self.player_name = player_name
        self.player_points = player_points

    def draw(self):
        pass

    def get_ui_widgets(self) -> UIWidgets:
        
        return UIWidgets(reg_widgets=[UILabel(text=f" {self.player_name} has won the game with {self.player_points} ",font_name=('Open Sans',),font_size=((SCREEN_WIDTH*(2/3))/len(f"{self.player_name} has won the game with {self.player_points}")),bold=True,text_color=(0,0,0,255)).with_space_around(bottom=SCREEN_WIDTH//7)],change_state_buttons=[(UIFlatButton(text="Back to Menu", width=SCREEN_WIDTH/3),0)])

class SettingsMenu(ToBeImplementedMenu):
    pass

class StatsMenu(ToBeImplementedMenu):
    pass


class RealStatsMenu(Menu):
    box_x:str = 'center'
    box_y:str = 'top'
    state:IntEnum = GameState(4)
    background_colour: arcade.color = arcade.color.ORANGE


    def __init__(self):
        self.stored_data:list[list[dict]] = []
        self.top:UIBoxLayout = UIBoxLayout()
        self.middle = UIBoxLayout()
        self.back:UIBoxLayout = UIBoxLayout() #store grid data when in other frame
        self.frame = UIBoxLayout()
        self.frame.add(self.top)
        


    def draw(self):
        pass

    def search(self,query='default'):
        self.stored_data = make_query(query)
        self.middle.clear()  
        for game in self.stored_data:
            text = ''
            for player in game['players']:
                text += player['name'] + ' vs '
            text = text[:-3] + "- " + game['dt'].strftime("%m/%d/%Y, %H:%M:%S")
            box = UIBoxLayout(vertical=False)
            label = UILabel(width=SCREEN_WIDTH*(4/5),height=SCREEN_HEIGHT//7,text=text,bold=True).with_space_around(bg_color=arcade.color.DARK_BLUE)
            view_btn = UIFlatButton(width=SCREEN_WIDTH*(1/5),height=SCREEN_HEIGHT//7,text='View')
            view_btn.on_click = lambda event,gme=game: self.find_more_stats(gme)
            box.add(label)
            box.add(view_btn)
            self.middle.add(box)

    def find_more_stats(self,game):
        self.frame.clear()
        self.frame.add(self.back)
        text = ''
        for player in game['players']:
            text += '_'*max((50-len(player['name']+ '-Stats'))//2,0) +player['name']+ '-Stats' +'_'*max((50-len(player['name']+ '-Stats'))//2,0) + '\n\n'
            text += f'Main words: {["".join(i["main_word"]["characters"]) for i in player["words"]]}' + '\n\n'
            text += f'Chain words: {["".join(i["characters"]) for j in player["words"] for i in j["chains"]]}' + '\n\n\n'
        text += '_'*20 +'Game-Stats' +'_'*20 + '\n\n'
        text += f"num_of_plays:{game['num_of_plays']}\nnum_of_shuffles{game['num_of_shuffles']}\nnum_of_challenges{game['num_of_challenges']}"
        
        text_area = UITextArea(width=(SCREEN_WIDTH*(2/3)),height=(SCREEN_HEIGHT*(2/3)),font_name=('Open Sans',),text=text,text_color=arcade.color.RED_DEVIL).with_space_around(bg_color=arcade.color.WHITE)
        button = UIFlatButton(text='Back to Grid',width=(SCREEN_WIDTH*(2/3)),height=(SCREEN_HEIGHT//10))
        button.on_click = lambda event: self.back.clear() or self.frame.clear() or self.frame.add(self.top)
        self.back.add(text_area)
        self.back.add(button)

    def get_ui_widgets(self) -> UIWidgets:
        query = MyInputText(width=SCREEN_WIDTH*(4/5),text="  INPUT DATE: YYYY/MM/DD  ",font_name=('Open Sans',),font_size=(SCREEN_WIDTH/35))
        self.query = query
        query = query.with_space_around(bg_color=arcade.color.WHITE)
       
        submit_btn = UIFlatButton(width=SCREEN_WIDTH*(1/5),text='Search')

        submit_btn.on_click = lambda event: self.search(self.query.text)
        submit_widgets = UIBoxLayout(vertical=False)
        submit_widgets.add(query)
        submit_widgets.add(submit_btn)
        submit_widgets = submit_widgets.with_space_around(bottom=SCREEN_HEIGHT//10)
        self.top.add(submit_widgets)
        self.top.add(self.middle)

        return UIWidgets(reg_widgets=[self.frame],change_state_buttons=[(UIFlatButton(text="Back to Menu", width=SCREEN_WIDTH/3),0)])

        
    





Menus = (SelectionMenu,SetupMenu1,SetupMenu2,GameMenu,GameFinishedMenu,SettingsMenu,RealStatsMenu)

