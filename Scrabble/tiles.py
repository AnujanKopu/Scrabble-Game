def make_letters(resize_val):
  from PIL import Image
  from PIL import ImageFont
  from PIL import ImageDraw 
  def make_tiles(letter,value,rsv):
    W,H = (114,104)
    msg = letter
    msg1= value

    img = Image.open("./Scrabble/tiles/extra/BLANK.png")
    draw = ImageDraw.Draw(img)
    # font = ImageFont.truetype(<font-file>, <font-size>)
    # draw.text((x, y),"Sample Text",(r,g,b))
    font = ImageFont.truetype("./Scrabble/tiles/extra/OpenSans.ttf", 65)
    w,h = draw.textsize(msg,font=font)
    draw.text(((W-w)/2, (H-h)/2),msg,(0,0,0),font=font)
    img.save("./Scrabble/tiles/extra/temp.png",quality=100)
    img = Image.open("./Scrabble/tiles/extra/temp.png")
    draw = ImageDraw.Draw(img)
    font1 = ImageFont.truetype("./Scrabble/tiles/extra/OpenSans.ttf", 30)
    w1,h1 = draw.textsize(msg1,font=font1)
    draw.text((W-w1-5,H-h1+5),msg1,(0,0,0),font=font1)
    #img.save('temp.png')
    #img = Image.open("temp.png")
    img = img.resize((rsv,rsv))
    img.save(f'./Scrabble/tiles/{letter}.png' if letter != " " else './Scrabble/tiles/BLANK.png',quality=100)
  
  letters = [('A',1), ('E',1), ('I',1),('L',1), ('N',1), ('O',1), ('R',1), ('S',1), ('T',1),('U',1), ('D',2),('G',2),('B',3), ('C',3), ('M',3),('P',3),('F',4),('H',4), ('V',4), ('W',4),('Y',4),('K',5),('J',8),('X',8),('Q',10),('Z',10) ]
  make_tiles(" "," ",resize_val)
  for char in letters:
    make_tiles(char[0],str(char[1]),resize_val)
    
