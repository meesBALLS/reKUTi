from tkinter       import Frame, Label, Button
import tkinter     as tk
import threading
import random
import time
from PIL.ImageDraw import Draw
from PIL.ImageTk   import PhotoImage
from PIL           import Image, ImageTk

scherm_size = 1000
plaatje_size = 600
grid_size = 6

offset = plaatje_size / grid_size / 10
straal = plaatje_size / grid_size - offset

beurt_speler = 1
vorige_zetten = []
zetten_tekenen = False
zetten_mogelijk = True
bots_aan = False

scherm = Frame()
scherm.master.title("reKUTi")
scherm.configure(background=("#654321"))

scherm.configure(width=scherm_size, height=scherm_size)
scherm.pack()

lijst1 = [(0)for i in range(0, grid_size**2)]

canvas = tk.Canvas(scherm, width=200, height=20)
canvas.place(x=700, y=100)

white_label = tk.Label(scherm, text="wit: 0", font=("Arial", 10))
white_label.place(x=620, y=100)
black_label = tk.Label(scherm, text="zwart: 0", font=("Arial", 10))
black_label.place(x=930, y=100)

turn_label = tk.Label(scherm, text="zwart is aan de beurt", font=("Arial", 10), fg="black")
turn_label.place(x=650, y=160)

input_field = tk.Entry(scherm)
input_field.place(x=650, y=200, width=167)
  
def bbc(event):
    if input_field.get().lower() == "bbc":
        circle_image = Image.open("Big_Black_Cock.jpeg")
        circle_image.show()

input_field.bind("<Return>", bbc)

plaatje = Image.new( mode="RGBA" , size=(plaatje_size,plaatje_size)) 
draw = Draw(plaatje)
afbeelding = Label(scherm) 
afbeelding.place(x=0, y=0) 
afbeelding.configure(width=plaatje_size, height=plaatje_size, bg="green")
afbeelding.configure(bg="green")

def beurt_knop_klik():
    global beurt_speler, zetten_tekenen
    beurt_speler = beurt_speler%2+1
    teken_zetten(3)
    teken_score()
    zetten_tekenen = False

def hulp_knop_klik():
    global beurt_speler, zetten_tekenen
    zetten_tekenen = not zetten_tekenen
    if zetten_tekenen:
        teken_zetten(beurt_speler%2+1)
    else:
        teken_zetten(3)

def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("!")
    label = tk.Label(popup, text=msg)
    label.pack(side="top", fill="x", pady=10)
    B1 = tk.Button(popup, text="Okay", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def lees_dropdown(_):
    global grid_size, lijst1, offset, straal
    #haalt de grid_size uit de dropdown
    grid_size = int(default.get().split("x")[0])
    draw.rectangle((0, 0, plaatje_size, plaatje_size), fill="green")
    #reset de lijst

    lijst1 = [(0)for i in range(0, grid_size**2)]
    
    offset = plaatje_size / grid_size / 10
    straal = plaatje_size / grid_size - offset 
    speelveld_tekenen(grid_size)

# lees in alle functies hieronder, tot snap_plaats, de _ als "naar"
# returned de index van de lijst waar de x en y coordinaten van de grid zijn
def grid_lijst(x,y):
    return -1 if x > grid_size or x<=0 or y<=0 or y > grid_size else grid_size*(y-1)+x-1

# returned de x en y coordinaten van de grid op de gegeven index
def lijst_grid(i):
    return (i%grid_size+1, i//grid_size+1)

# veranderd de waarde van de lijst op de gegeven index naar de gegeven speler
def speler_lijst(x, y, speler):
    lijst1[grid_size*(y-1)+x-1] = speler
  
# returned de x en y coordinaten van de grid op de gegeven scherm coordinaten
def scherm_grid(x,y):
    omzetting = lambda a : round(a / (plaatje_size / grid_size) + 1)  # noqa: E731
    return (omzetting(x), omzetting(y))

def grid_scherm(x,y):
    omzetting = lambda a : (a-1)*(plaatje_size/grid_size)  # noqa: E731
    return (omzetting(x), omzetting(y))

# snapt de gegeven scherm coordinaten naar de dichtsbijzijnde hoek coordinaten
def snap_plaats(x,y):
    omzetting = lambda a : a % (plaatje_size / grid_size)  # noqa: E731
    return (x-omzetting(x),y-omzetting(y))

def teken_score():
    # calculate the percentage of stones for each player
    total_stones = lijst1.count(1) + lijst1.count(2)
    try :
        black_percentage = lijst1.count(1) / total_stones
    except ZeroDivisionError:
        black_percentage = 0
    
    canvas.create_rectangle(0, 0, 200 * black_percentage, 20, fill="white")
    canvas.create_rectangle(200 * black_percentage, 0, 200, 20, fill="black")
    white_label.config(text=f"wit: {lijst1.count(1)}")
    black_label.config(text=f"zwart: {lijst1.count(2)}")
    turn_label.config(text="zwart is aan de beurt" if beurt_speler == 2 else "wit is aan de beurt",fg="black" if beurt_speler == 2 else "white", bg="grey", width=20)

def speelveld_tekenen(veld_grootte):
    global plaatje_size
    lijn_pos = plaatje_size / veld_grootte
    #tekent de lijnen die het speelveld vormen
    for i in range(1,veld_grootte):
        draw.line(((lijn_pos*i,0),(lijn_pos*i,plaatje_size)),fill="black")
        draw.line(((0,lijn_pos*i),(plaatje_size,lijn_pos*i)),fill="black")
    
    begin_stukken(veld_grootte)
    teken_score()

def begin_stukken(veld_grootte):
    center = plaatje_size / 2
    teken_stuk(center, center, 1, True)
    teken_stuk(center-plaatje_size/veld_grootte, center, 2, True)
    teken_stuk(center, center-plaatje_size/veld_grootte, 2, True)
    teken_stuk(center-plaatje_size/veld_grootte, center-plaatje_size/veld_grootte, 1, True)

def omliggende_check(speler):
    lege_plaatsen = set()
    
    andere_speler = speler
    speler = (speler)%2 +1
    
    delta = [-1, 0, 1, 0, -1, -1, 1, 1, -1] # 8 richtingen
    grid_squared = grid_size**2
    for i in range(0,grid_squared):
        if lijst1[i] == speler:
            x,y = lijst_grid(i)
            for j in range(8):          
                dx, dy = delta[j], delta[j+1]
                if (x+dx and y+dy ) <= grid_size and (x+dx and y+dy) >= 0 and lijst1[(grid_lijst(x+dx,y+dy))] == andere_speler:
                    for k in range(1,grid_size):
                        new_x, new_y = x+k*dx, y+k*dy
                        if (new_x or new_y ) > grid_size or (new_x or new_y) < 0:
                            break
                        elif lijst1[grid_lijst(new_x, new_y)] == speler:
                            break
                        elif lijst1[grid_lijst(new_x, new_y)] == 0:
                            lege_plaatsen.add((new_x, new_y))
                            break
    
    return lege_plaatsen

def teken_zetten(speler):
    if vorige_zetten != []:
        for i in vorige_zetten:
            a=i[0]
            b=i[1]
            if lijst1[grid_lijst(a,b)] == 0:
                a,b = grid_scherm(a,b)
                a += offset//2
                b+= offset//2
                draw.rectangle((a, b, a+straal, b+straal), fill="green")
    if omliggende_check(speler) == set() and speler!=3:
        popupmsg("geen zetten mogelijk, druk op beurt overslaan")
    else: 
        for i in omliggende_check(speler):
            a,b = i
            vorige_zetten.append((a,b))
            a,b = grid_scherm(a,b)

            a += offset*4
            b += offset*4
            draw.ellipse(((a,b),(a+straal/5,b+straal/5)),outline="Red", width=5)
    
    global foto
    foto = ImageTk.PhotoImage(plaatje)
    afbeelding.configure(image=foto)

def stukken_veranderen(speler, x, y):
    andere_speler = speler % 2 + 1
    delta = [-1, 0, 1, 0, -1, -1, 1, 1, -1] # 8 richtingen
    for j in range(8):
        dx, dy = delta[j], delta[j+1]
        geslagen_stukken = []
        if (x+dx and y+dy ) <= grid_size and (x+dx and y+dy) > 0 and lijst1[(grid_lijst(x+dx,y+dy))] == andere_speler:
            for k in range(1,grid_size):
                
                new_x, new_y = x+k*dx, y+k*dy
                if (new_x or new_y) > grid_size or (new_x or new_y) <1 or lijst1[grid_lijst(new_x, new_y)] == 0:
                    print("buiten kut")
                    break
                elif lijst1[grid_lijst(new_x, new_y)] == andere_speler:
                    if x+(k+1)*dx > grid_size or y+(k+1)*dy > grid_size or x+((k+1)*dx) <1 or y+((k+1)*dy) < 1 or lijst1[grid_lijst(x+((k+1)*dx),y+((k+1)*dy))]==0:
                        break
                    else:
                        geslagen_stukken.append((new_x, new_y))
                elif lijst1[grid_lijst(new_x, new_y)] == speler:
                    for i in geslagen_stukken:
                        teken_stuk(*grid_scherm(i[0],i[1]),speler = speler,computer = True, kut_recursie=False)
                        speler_lijst(*i,speler)
                    break         

def teken_stuk(x,y,speler, computer=False, kut_recursie=True):
    global beurt_speler
    
    x,y = snap_plaats(x,y)
    grid_x, grid_y = scherm_grid(x,y)

    x += offset//2
    y += offset//2  
    
    # checkt of de grid positie al bezet is
    if lijst1[grid_lijst(grid_x,grid_y)] != 0 and computer is not True:
        return

    if (grid_x,grid_y) not in [opties for opties in omliggende_check((speler%2+1))] and computer is False:
        print("niet mogelijk om hier te plaatsen")
        return
    if kut_recursie:
        stukken_veranderen(beurt_speler, grid_x, grid_y)
    speler_lijst(grid_x,grid_y,speler)
    
    if speler == 1:
        draw.ellipse(((x,y),(x+straal,y+straal)),fill="White")
        beurt_speler = 2
    elif speler == 2:
        draw.ellipse(((x,y),(x+straal,y+straal)),fill="Black")
        beurt_speler = 1
        
    global foto
    foto = ImageTk.PhotoImage(plaatje)
    afbeelding.configure(image=foto)

def winner(speler):
    if len(omliggende_check(speler)) == 0 and len(omliggende_check(speler%2+1)) == 0:
        teken_score()
        if lijst1.count(1) <lijst1.count(2):
            circle_image = Image.open("Big_Black_Cock.jpeg")
            circle_image.show()
        popupmsg("gelijkspel" if lijst1.count(1)==lijst1.count(2) 
                else ("zwart wint" if lijst1.count(1) <lijst1.count(2) else "wit wint"))

def bot_zet():
    global beurt_speler
    legal_positions = omliggende_check(beurt_speler%2+1)
    print(legal_positions)
    if len(legal_positions) == 0:
        beurt_speler = beurt_speler%2+1
        return
    
    x, y = random.choice(list(legal_positions))
    print(x,y)
    if x>grid_size or y>grid_size or x<1 or y<1:
        print("kut")
        beurt_speler = beurt_speler%2+1
        return
 
    print(x,y)
    if 0< x <= grid_size and 0< y <= grid_size:
        
        muisKlik(type("Event", (), {"x": grid_scherm(x,y)[0], "y": grid_scherm(x,y)[1]}))  

def bvb_thread():
    global beurt_speler
    while bots_aan:
        bot_zet()
        
        if len(omliggende_check(beurt_speler%2+1)) == 0:
            beurt_speler = beurt_speler%2+1
            bot_zet()

        time.sleep(0.2)
    
        
def bvb_klik():
    global bots_aan
    botvsbot_knop.config(text="stop")

    if not bots_aan:
        bots_aan = True
        t1 = threading.Thread(target=bvb_thread)
        t1.start()
    else:
        
        bots_aan = False
        botvsbot_knop.config(text="bot vs bot")

def bot_klik():
    bot_zet()
    
def muisKlik(ea):
    global beurt_speler, zetten_tekenen
    t1 = threading.Thread(target=omliggende_check, args=(beurt_speler,))
    t1.start()
    teken_stuk(ea.x,ea.y,beurt_speler)
    zetten_tekenen = False
    teken_zetten(3)
    winner(beurt_speler)
    teken_score()
    t1.join()
    
default = tk.StringVar(scherm)
default.set("6x6")
opties = ["4x4","6x6", "8x8", "10x10", "20x20", "30x30"]
drop = tk.OptionMenu(scherm, default,*opties)
drop.place(x=0, y=620)
beurt_knop = Button(scherm, text="beurt overslaan", command=beurt_knop_klik)
beurt_knop.place(x=650, y=30)
bot_knop = Button(scherm, text="bot", command=bot_klik)
bot_knop.place(x=650, y=0)
botvsbot_knop = Button(scherm, text="bot vs bot", command=bvb_klik)
botvsbot_knop.place(x=700, y=0)
nieuw_spel_knop = Button(scherm, text="nieuw spel", command=lambda: lees_dropdown(0))
nieuw_spel_knop.place(x=80, y=620)
hulp_knop = Button(scherm, text="help", command=hulp_knop_klik)
hulp_knop.place(x=650, y=60)

speelveld_tekenen(grid_size)
afbeelding.bind("<Button-1>", muisKlik)
scherm.mainloop()