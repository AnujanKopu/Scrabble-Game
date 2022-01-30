
from config import *
from menus import (
  Menus,
  UIWidgets
)
from tiles import make_letters

import arcade   

from arcade.gui import (
  UIManager,
  UIBoxLayout,
  UIAnchorWidget,

)



class Display(arcade.Window):
  
    def __init__(self):
        # Setup the window by initializing the parent class

        """Setting up the basic display properties needed for the game"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.manager = UIManager() #Built in ui manager used to create buttons and text fields
        self.manager.enable()
        self.box = UIBoxLayout()
        self.anchor = UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.box)
        
        self.manager.add(self.anchor)


    def connect_widgets(self,widgets:UIWidgets,box:UIBoxLayout):
      for i in widgets.reg_widgets:
        box.add(i)

      for i in widgets.change_state_buttons: 
        i[0].on_click = lambda event, value=i[1]: self.menu.validate() or self.change_state(value,self.menu.get_next_stage_info()) #Validate will return 0 to change state or 1 if not.
        box.add(i[0])

      if not widgets.exit_button is None: 
        widgets.exit_button.on_click = lambda event: arcade.exit()
        box.add(widgets.exit_button)


    def change_state(self,state,extra_info=None):
      self.box.clear()
      self.set_viewport(0,SCREEN_WIDTH,0,SCREEN_HEIGHT)
      self.menu = Menus[state](*extra_info) if not extra_info is None else Menus[state]()
      self.connect_widgets(self.menu.get_ui_widgets(),self.box)
      self.anchor.anchor_x,self.anchor.anchor_y = self.menu.box_x,self.menu.box_y
      arcade.set_background_color(self.menu.background_colour)



    def on_draw(self):
      arcade.start_render()
      self.menu.draw()
      self.manager.draw()


    def setup(self):
      self.change_state(0)
      pass


    def on_update(self,delta_time:float):
      result = self.menu.on_update(delta_time)
      if result is None: return
      if result[0] == 'center':self.set_viewport(0,SCREEN_WIDTH,0,SCREEN_HEIGHT)
      elif result[0] == 'change_state':self.change_state(result[1],result[2])
 
    def on_key_press(self, symbol: int, modifiers: int):
        self.menu.on_key_press(symbol,modifiers)

  
    
    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, button: int, modifiers: int):
        if self.menu.on_mouse_drag(x,y,dx,dy,button,modifiers) and button == 4:
          a,b,c,d = self.get_viewport()
          self.set_viewport(min(SCREEN_WIDTH//2,max(-(SCREEN_WIDTH//2),a-dx)),min(max(SCREEN_WIDTH//2,b-dx),3*SCREEN_WIDTH//2),min(max(-(SCREEN_HEIGHT//2),c-dy),SCREEN_HEIGHT//2),min(max(SCREEN_HEIGHT//2,d-dy),3*SCREEN_HEIGHT//2))
          self.menu.screenoffset.x,self.menu.screenoffset.y = (min(SCREEN_WIDTH//2,max(-(SCREEN_WIDTH//2),a-dx)),min(max(-(SCREEN_HEIGHT//2),c-dy),SCREEN_HEIGHT//2))



    def on_mouse_scroll(self,x,y,sx,sy):
      self.menu.on_mouse_scroll(x,y,sx,sy)
      #global CAMERA_HEIGHT,CAMERA_WIDTH
      #CAMERA_WIDTH -= sx
      #CAMERA_HEIGHT -= sy


    
    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
      self.menu.on_mouse_press(x,y,button,modifiers)

      


    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
      self.menu.on_mouse_release(x,y,button,modifiers)




def start():
  make_letters(int(GB_LEN//16)+1)
  window = Display()
  window.setup()
  arcade.run()
