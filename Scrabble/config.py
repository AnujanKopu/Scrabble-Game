from arcade import load_texture

SCREEN_WIDTH = SCREEN_HEIGHT = 900  #Max 2600 x 2600 
SCREEN_TITLE = "Scrabble"



GB_LEN = int(SCREEN_HEIGHT*0.7)
GB = load_texture("./Scrabble/textures/board.png")#Game board

PD_LENGTH,PD_HEIGHT = int(GB_LEN//15)*7,int(GB_LEN//15)#Player deck 

