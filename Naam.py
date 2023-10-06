from tkinter       import Frame, Label
import tkinter as tk
from PIL.ImageDraw import Draw
from PIL.ImageTk   import PhotoImage
from PIL           import Image, ImageTk

scherm_size = 1000
plaatje_size = 600
speelveld_grootte = 6

offset = plaatje_size / speelveld_grootte / 10
straal = plaatje_size / speelveld_grootte - offset

beurt_speler = 1

scherm = Frame()
scherm.master.title("reKUTi")
scherm.configure(background="lightblue")
scherm.configure(width=scherm_size, height=scherm_size)
scherm.pack()

default = tk.StringVar(scherm)
default.set("6x6")



def lees_dropdown(heu):
    global speelveld_grootte
    speelveld_grootte = int(default.get().split("x")[0])
    
    cirkel_lijst.clear()
    
    draw.rectangle((0, 0, plaatje_size, plaatje_size), fill="white")
    Speelveld_tekenen(speelveld_grootte)

opties = ["6x6", "8x8", "10x10", "20x20", "30x30"]
drop = tk.OptionMenu(scherm, default,*opties, command=lees_dropdown)
drop.place(x=0, y=600)

plaatje = Image.new( mode="RGBA" , size=(plaatje_size,plaatje_size)) 
draw = Draw(plaatje)

afbeelding = Label(scherm) 
afbeelding.place(x=0, y=0) 
afbeelding.configure(width=plaatje_size, height=plaatje_size)

class cirkel_info:
    def __init__(self,x,y,speler):
        self.x = x
        self.y = y
        self.speler = speler
        
    def __str__(self):
        return f"x={self.x} y={self.y} speler={self.speler}"
    
    def __repr__(self):
        return str(self)

cirkel_lijst = []


def Speelveld_tekenen(x):
    global plaatje_size
    lijn_pos = plaatje_size / x
    for i in range(1,x):
        draw.line(((lijn_pos*i,0),(lijn_pos*i,plaatje_size)),fill="black")
        draw.line(((0,lijn_pos*i),(plaatje_size,lijn_pos*i)),fill="black")
    
    global offset, straal
    offset = plaatje_size / speelveld_grootte / 10
    straal = plaatje_size / speelveld_grootte - offset   
    
    center = plaatje_size / 2
    teken_stuk(center, center, 1)
    teken_stuk(center-plaatje_size/x, center, 2)
    teken_stuk(center, center-plaatje_size/x, 2)
    teken_stuk(center-plaatje_size/x, center-plaatje_size/x, 1)
    


def teken_stuk(x,y,speler):
    global beurt_speler    

    x -= x % (plaatje_size / speelveld_grootte)
    y -= y % (plaatje_size / speelveld_grootte) 
    
    grid_x = x / (plaatje_size/speelveld_grootte) + 1
    grid_y = y / (plaatje_size/speelveld_grootte) + 1
    
    
    for i in cirkel_lijst:
        if i.x == grid_x and i.y == grid_y:
            print("niet mogelijk om hier te plaatsen")
            return
    
    x += offset//2
    y += offset//2  
    
    cirkel_lijst.append(cirkel_info(grid_x,grid_y,beurt_speler))
    if speler == 1:
        beurt_speler = 2
        circle_image = Image.open("Screenshot 1 v2.png")
        circle_image = circle_image.resize((int(straal), int(straal)))
        #draw.ellipse(((x,y),(x+straal,y+straal)),fill="Blue")
        draw.bitmap((x, y), circle_image.convert('RGBA'))
    elif speler == 2:
        circle_image = Image.open("Screenshot1.png")
        circle_image = circle_image.resize((int(straal), int(straal)))
        #draw.ellipse(((x,y),(x+straal,y+straal)),fill="Red")
        draw.bitmap((x, y), circle_image.convert('RGBA'))
        beurt_speler = 1
        
        
    
    global foto
    foto = ImageTk.PhotoImage(plaatje)
    afbeelding.configure(image=foto)


    
def muisKlik(ea):
    global beurt_speler 
    teken_stuk(ea.x,ea.y,beurt_speler)
       
    #print(cirkel_lijst)


# een Label kan ook gebruikt worden om een PhotoImage te laten zien
Speelveld_tekenen(speelveld_grootte)
afbeelding.bind("<Button-1>", muisKlik)
scherm.mainloop()
