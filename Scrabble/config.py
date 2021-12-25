from arcade import load_texture

SCREEN_WIDTH,SCREEN_HEIGHT,SCREEN_TITLE =900, 900,"Scrabble" #Max 2600 x 2600 
#CAMERA_WIDTH,CAMERA_HEIGHT = 600,600


GB_LEN = int(SCREEN_HEIGHT*0.7)
GB = load_texture("./Scrabble/textures/board.png")#Game board

PD_LENGTH,PD_HEIGHT = int(GB_LEN//15)*7,int(GB_LEN//15)#Player deck 


board= [[None for i in range(15)] for i in range(15)]