from tkinter       import Frame, Label
import tkinter     as tk
from PIL.ImageDraw import Draw
from PIL.ImageTk   import PhotoImage
from PIL           import Image, ImageTk

scherm_size = 1000
plaatje_size = 600
grid_size = 6

offset = plaatje_size / grid_size / 10
straal = plaatje_size / grid_size - offset

beurt_speler = 1

scherm = Frame()
scherm.master.title("reKUTi")
scherm.configure(background="lightblue")
scherm.configure(width=scherm_size, height=scherm_size)
scherm.pack()

lijst1 = [(0)for i in range(0, grid_size**2)]
lege_plaatsen = []

def lees_dropdown(_):
    global grid_size, lijst1, offset, straal
    #haalt de grid_size uit de dropdown
    grid_size = int(default.get().split("x")[0])
    draw.rectangle((0, 0, plaatje_size, plaatje_size), fill="white")
    #reset de lijst
    lijst1 = [(0)for i in range(0, grid_size**2)]
    
    offset = plaatje_size / grid_size / 10
    straal = plaatje_size / grid_size - offset 
    speelveld_tekenen(grid_size)
    
default = tk.StringVar(scherm)
default.set("6x6")
opties = ["6x6", "8x8", "10x10", "20x20", "30x30"]
drop = tk.OptionMenu(scherm, default,*opties, command=lees_dropdown)
drop.place(x=0, y=600)

plaatje = Image.new( mode="RGBA" , size=(plaatje_size,plaatje_size)) 
draw = Draw(plaatje)
afbeelding = Label(scherm) 
afbeelding.place(x=0, y=0) 
afbeelding.configure(width=plaatje_size, height=plaatje_size)

# lees in alle functies hieronder, tot snap_plaats, de _ als "naar"
# returned de index van de lijst waar de x en y coordinaten van de grid zijn
def grid_lijst(x,y):
    if x > grid_size or x<0 or y<0 or y > grid_size:
        return
    return grid_size*(y-1)+x-1

# returned de x en y coordinaten van de grid op de gegeven index
def lijst_grid(i):
    return (i%grid_size+1, i//grid_size+1)

# veranderd de waarde van de lijst op de gegeven index naar de gegeven speler
def speler_lijst(x, y, speler):
    lijst1[grid_lijst(x,y)] = speler

# returned de x en y coordinaten van de grid op de gegeven scherm coordinaten
def scherm_grid(x,y):
    omzetting = lambda a : round(a / (plaatje_size / grid_size) + 1)  # noqa: E731
    return (omzetting(x), omzetting(y))

# snapt de gegeven scherm coordinaten naar de dichtsbijzijnde hoek coordinaten
def snap_plaats(x,y):
    omzetting = lambda a : a % (plaatje_size / grid_size)  # noqa: E731
    return (x-omzetting(x),y-omzetting(y))

def speelveld_tekenen(veld_grootte):
    global plaatje_size
    lijn_pos = plaatje_size / veld_grootte
    #tekent de lijnen die het speelveld vormen
    for i in range(1,veld_grootte):
        draw.line(((lijn_pos*i,0),(lijn_pos*i,plaatje_size)),fill="black")
        draw.line(((0,lijn_pos*i),(plaatje_size,lijn_pos*i)),fill="black")
    
    begin_stukken(veld_grootte)

def begin_stukken(veld_grootte):
    center = plaatje_size / 2
    teken_stuk(center, center, 1)
    teken_stuk(center-plaatje_size/veld_grootte, center, 2)
    teken_stuk(center, center-plaatje_size/veld_grootte, 2)
    teken_stuk(center-plaatje_size/veld_grootte, center-plaatje_size/veld_grootte, 1)

def omliggende_check(i, speler):
    x,y = lijst_grid(i)
    andere_speler = (speler)%2 +1
    delta = [-1, 0, 1, 0, -1, -1, 1, 1, -1] # 8 richtingen
    for j in range(8):
        print(x,y)
        if x+delta[j] > grid_size or x+delta[j] < 0 or y+delta[j+1] > grid_size or y+delta[j+1] < 0:
            print("buiten bereik")
            pass
        elif lijst1[(grid_lijst(x+delta[j],y+delta[j+1]))] == andere_speler:
            print("andere", x+delta[j],y+delta[j+1])
            
        elif lijst1[grid_lijst(x+delta[j],y+delta[j+1])] == speler:
            print("je eigen stenen",x+delta[j],y+delta[j+1])
            
        else:
            lege_plaatsen.append((x+delta[j],y+delta[j+1]))

def teken_stuk(x,y,speler):
    global beurt_speler    
    
    x,y = snap_plaats(x,y)
    grid_x, grid_y = scherm_grid(x,y)
        
    omliggende_check(grid_lijst(grid_x,grid_y), speler)
    # oude code
        # for i in lijst1:
        #     if lijst1[i] == grid_lijst(grid_x,grid_y):
        #         print("niet mogelijk om hier te plaatsen")
        #         return
    x += offset//2
    y += offset//2  
    
    # checkt of de grid positie al bezet is
    if lijst1[grid_lijst(grid_x,grid_y)] != 0:
        print("niet mogelijk om hier te plaatsen")
        return
    
    speler_lijst(grid_x,grid_y,speler)
    # speler logica
    if speler == 1:
        #circle_image = Image.open("Screenshot 1 v2.png")
        #circle_image = circle_image.resize((int(straal), int(straal)))
        #draw.bitmap((x, y), circle_image.convert('RGB'))
        
        draw.ellipse(((x,y),(x+straal,y+straal)),fill="Blue")
        beurt_speler = 2
    elif speler == 2:
        #circle_image = Image.open("Screenshot1.png")
        #circle_image = circle_image.resize((int(straal), int(straal)))
        #draw.bitmap((x, y), circle_image.convert('RGB'))
        
        draw.ellipse(((x,y),(x+straal,y+straal)),fill="Red")
        beurt_speler = 1
        
    global foto
    foto = ImageTk.PhotoImage(plaatje)
    afbeelding.configure(image=foto)

def muisKlik(ea):
    global beurt_speler 
    teken_stuk(ea.x,ea.y,beurt_speler)

# een Label kan ook gebruikt worden om een PhotoImage te laten zien
speelveld_tekenen(grid_size)
afbeelding.bind("<Button-1>", muisKlik)
scherm.mainloop()
