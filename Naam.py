from tkinter       import Frame, Label
import tkinter     as tk
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

cirkel_lijst = []

lijst1 = [(0)for i in range(0, speelveld_grootte**2)]

def lees_dropdown(heu):
    global speelveld_grootte
    global lijst1
    speelveld_grootte = int(default.get().split("x")[0])
    
    cirkel_lijst.clear()
    lijst1 = [(0)for i in range(0, speelveld_grootte**2)]
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

# class cirkel_info:
#     def __init__(self,x,y,speler):
#         self.x = x
#         self.y = y
#         self.speler = speler
        
#     def __str__(self):
#         return f"x={self.x} y={self.y} speler={self.speler}"
    
#     def __repr__(self):
#         return str(self)


# returned de index van de lijst corensponderend met de x en y coordinaten
def locatie_omzetten(x,y):
    if x > speelveld_grootte or x<0 or y<0 or y > speelveld_grootte:
        return 
    return speelveld_grootte*(y-1)+x-1
# returned de x en y coordinaten van de lijst corensponderend met de index
def coordinaten(i):
    return (i%speelveld_grootte+1, i//speelveld_grootte+1)
# zorgt dat de zet in lijst1 wordt geplaatst
def plaatsen(x, y, speler):
    lijst1[locatie_omzetten(x,y)] = speler



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


def hokjes(speler):
    lege_plaatsen = set()
    andere_speler = speler
    speler = (speler)%2 +1
    delta = [-1, 0, 1, 0, -1, -1, 1, 1, -1] # 8 richtingen
    for i in range(0,len(lijst1)):
        if lijst1[i] == speler:
            x,y = coordinaten(i)
            for j in range(8):               
                if x+delta[j] > speelveld_grootte or x+delta[j] < 0 or y+delta[j+1] > speelveld_grootte or y+delta[j+1] < 0:
                    print("buiten bereik")                   
                elif lijst1[(locatie_omzetten(x+delta[j],y+delta[j+1]))] == andere_speler:
                    for k in range(1,min(x+delta[j]%speelveld_grootte, y+delta[j+1]%speelveld_grootte)):
                        if x+k*delta[j] > speelveld_grootte or x+k*delta[j] <= 0 or y+k*delta[j+1] > speelveld_grootte or y+k*delta[j+1] <= 0:
                            break
                        elif lijst1[locatie_omzetten(x+k*delta[j], y+k*delta[j+1])] == 0:
                            lege_plaatsen.add((x+k*delta[j], y+k*delta[j+1]))
                            break
    print("lege mogelijke plaatsen", lege_plaatsen)
    for opties in lege_plaatsen:
        x,y = opties
        x = round((x -1)*(plaatje_size/speelveld_grootte))
        y = round((y -1)*(plaatje_size/speelveld_grootte))
    
        draw.ellipse(((x,y),(x+straal/10,y+straal/10)),fill="Grey")
                    

def teken_stuk(x,y,speler):
    global beurt_speler    

    x -= x % (plaatje_size / speelveld_grootte)
    y -= y % (plaatje_size / speelveld_grootte) 
    
    grid_x = round(x / (plaatje_size/speelveld_grootte) + 1)
    grid_y = round(y / (plaatje_size/speelveld_grootte) + 1)
    
    
    #oude code
        # for i in lijst1:
        #     if lijst1[i] == locatie_omzetten(grid_x,grid_y):
        #         print("niet mogelijk om hier te plaatsen")
        #         return
    x += offset//2
    y += offset//2  
    if lijst1[locatie_omzetten(grid_x,grid_y)] != 0:
        print("niet mogelijk om hier te plaatsen")
        return
    plaatsen(grid_x,grid_y,speler)
    hokjes(speler)
    if speler == 1:
        lijst1[locatie_omzetten(grid_x, grid_y)] = 1
        beurt_speler = 2
        circle_image = Image.open("Screenshot 1 v2.png")
        circle_image = circle_image.resize((int(straal), int(straal)))
        draw.ellipse(((x,y),(x+straal,y+straal)),fill="Blue")
        # draw.bitmap((x, y), circle_image.convert('RGBA'))
    elif speler == 2:
        lijst1[locatie_omzetten(grid_x, grid_y)] = 2
        circle_image = Image.open("Screenshot1.png")
        circle_image = circle_image.resize((int(straal), int(straal)))
        draw.ellipse(((x,y),(x+straal,y+straal)),fill="Red")
        # draw.bitmap((x, y), circle_image.convert('RGBA'))
        beurt_speler = 1
    
        
    # print(lijst1)
    global foto
    foto = ImageTk.PhotoImage(plaatje)
    afbeelding.configure(image=foto)



def muisKlik(ea):
    global beurt_speler 
    teken_stuk(ea.x,ea.y,beurt_speler)
    



# een Label kan ook gebruikt worden om een PhotoImage te laten zien
Speelveld_tekenen(speelveld_grootte)
afbeelding.bind("<Button-1>", muisKlik)
scherm.mainloop()
