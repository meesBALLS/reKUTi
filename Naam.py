from tkinter       import Frame, Label
from PIL.ImageDraw import Draw
from PIL.ImageTk   import PhotoImage
from PIL           import Image

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
    
    center = (x / 2)*100
    teken_stuk(center, center, 1)
    teken_stuk(center-100, center, 2)
    teken_stuk(center, center-100, 2)
    teken_stuk(center-100, center-100, 1)
        
    global foto
    foto = PhotoImage(plaatje)
    afbeelding.configure(image=foto)



def teken_stuk(x,y,speler):
    global beurt_speler
    
    x -= x % (plaatje_size / speelveld_grootte)
    y -= y % (plaatje_size / speelveld_grootte) 
    x += offset//2
    y += offset//2
    
    grid_x = x / (plaatje_size / speelveld_grootte) + 0.95
    grid_y = y / (plaatje_size / speelveld_grootte) + 0.95
    
    
    for i in cirkel_lijst:
        if i.x == grid_x and i.y == grid_y:
            print("niet mogelijk om hier te plaatsen")
            return
            
    
    
    cirkel_lijst.append(cirkel_info(grid_x,grid_y,1))
    if speler == 1:
      draw.ellipse(((x,y),(x+straal,y+straal)),fill="red")
    elif speler == 2:
      draw.ellipse(((x,y),(x+straal,y+straal)),fill="blue")
      
    if beurt_speler == 1:
      beurt_speler = 2
    elif beurt_speler == 2:
        beurt_speler = 1
    
    global foto
    foto = PhotoImage(plaatje)
    afbeelding.configure(image=foto)
    

    
    
    
def muisKlik(ea):
    global beurt_speler 
    teken_stuk(ea.x,ea.y,beurt_speler)
       
    
    print(cirkel_lijst)
        # add this code block below the existing code


# een Label kan ook gebruikt worden om een PhotoImage te laten zien

Speelveld_tekenen(speelveld_grootte)
afbeelding.bind("<Button-1>", muisKlik)
scherm.mainloop()
