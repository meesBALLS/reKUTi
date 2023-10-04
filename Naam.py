from tkinter       import Frame, Label
from PIL.ImageDraw import Draw
from PIL.ImageTk   import PhotoImage
from PIL           import Image

scherm_size = 1000
plaatje_size = 600
speelveld_grootte = 6

scherm = Frame()
scherm.master.title("reKUTi")
scherm.configure(background="lightblue")
scherm.configure(width=scherm_size, height=scherm_size)
scherm.pack()

plaatje = Image.new( mode="RGBA" , size=(plaatje_size,plaatje_size)) 
draw = Draw(plaatje)

afbeelding = Label(scherm) 
afbeelding.place(x=0, y=0) 
afbeelding.configure(width=plaatje_size, height=plaatje_size)



def Speelveld_tekenen(x):
    global plaatje_size
    lijn_pos = plaatje_size / x
    print(lijn_pos)
    for i in range(1,x):
        draw.line(((lijn_pos*i,0),(lijn_pos*i,plaatje_size)),fill="blue")
        draw.line(((0,lijn_pos*i),(plaatje_size,lijn_pos*i)),fill="blue")
    global foto
    foto = PhotoImage(plaatje)
    afbeelding.configure(image=foto)


def teken_stukken(x,y,speler):
    if speler == 1:
      draw.ellipse(((x,y),(x+600/speelveld_grootte,y+600/speelveld_grootte)),fill="red")
    elif speler == 2:
      draw.ellipse(((x,y),(x+600/speelveld_grootte,y+600/speelveld_grootte)),fill="blue")
    global foto
    foto = PhotoImage(plaatje)
    afbeelding.configure(image=foto)
    

Speelveld_tekenen(speelveld_grootte)


def muisKlik(ea):
    teken_stukken(ea.x,ea.y,1)


# een Label kan ook gebruikt worden om een PhotoImage te laten zien

afbeelding.bind("<Button-1>", muisKlik)
scherm.mainloop()
