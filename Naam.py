import tkinter     as tk
import threading
import random
import time
from PIL.ImageDraw import Draw
from PIL           import Image, ImageTk

scherm_size = 1000
plaatje_size = 600
grid_size = 6

# offset is om de stenen in het midden van de vakjes te plaatsen
offset = plaatje_size / grid_size / 10
straal = plaatje_size / grid_size - offset

beurt_speler = 1
vorige_zetten = []
zetten_tekenen = False
zetten_mogelijk = True
bots_aan = False

scherm = tk.Frame()
scherm.master.title("reKUTi")
scherm.configure(background=("#654321"))

scherm.configure(width=scherm_size, height=scherm_size)
scherm.pack()

lijst1 = [(0)for _ in range(0, grid_size**2)]

# canvas voor de wit zwarte balk
canvas = tk.Canvas(scherm, width=200, height=20)
canvas.place(x=700, y=100)

white_label = tk.Label(scherm, text="wit: 0", font=("Arial", 10))
white_label.place(x=620, y=100)
black_label = tk.Label(scherm, text="zwart: 0", font=("Arial", 10))
black_label.place(x=930, y=100)

turn_label = tk.Label(scherm, text="zwart is aan de beurt", font=("Arial", 10), fg="black")
turn_label.place(x=650, y=160)

plaatje = Image.new( mode="RGBA" , size=(plaatje_size,plaatje_size)) 
draw = Draw(plaatje)
afbeelding = tk.Label(scherm) 
afbeelding.place(x=0, y=0) 
afbeelding.configure(width=plaatje_size, height=plaatje_size, bg="green")
afbeelding.configure(bg="green")

""" ter informatie, teken_zetten(3) tekent zetten voor speler 3, maar die is er niet dus tekent hij geen zetten.
    beurt_speler = beurt_speler%2+1 zorgt ervoor dat de speler wisselt tussen 1 en 2
"""

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
    label.pack(side="top", fill="x", pady=20)
    B1 = tk.Button(popup, text="YAY", command = popup.destroy)
    B1.pack()
    popup.mainloop()

def lees_dropdown():
    global grid_size, lijst1, offset, straal
    #haalt de grid_size uit de dropdown
    grid_size = int(default.get().split("x")[0])
    draw.rectangle((0, 0, plaatje_size, plaatje_size), fill="green")
    
    #reset de lijst
    lijst1 = [(0)for _ in range(0, grid_size**2)]
    
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
    # bepaalt het zwart percentage
    total_stones = lijst1.count(1) + lijst1.count(2)
    try :
        black_percentage = lijst1.count(1) / total_stones
    except ZeroDivisionError:
        black_percentage = 0
    # de huidige status van de game weergeven
    canvas.create_rectangle(0, 0, 200 * black_percentage, 20, fill="white")
    canvas.create_rectangle(200 * black_percentage, 0, 200, 20, fill="black")
    white_label.config(text=f"wit: {lijst1.count(1)}")
    black_label.config(text=f"zwart: {lijst1.count(2)}")
    turn_label.config(text="zwart is aan de beurt" if beurt_speler == 2
                      else "wit is aan de beurt",
                      fg="black" if beurt_speler == 2 
                      else "white", bg="grey", width=20)

def speelveld_tekenen(veld_grootte):
    global plaatje_size
    lijn_pos = plaatje_size / veld_grootte
    #tekent de lijnen die het speelveld vormen
    for i in range(1,veld_grootte):
        draw.line(((lijn_pos*i,0),(lijn_pos*i,plaatje_size)),fill="black")
        draw.line(((0,lijn_pos*i),(plaatje_size,lijn_pos*i)),fill="black")
    #omdat we een heel nieuw plaatje tekenen moeten ook de stenen opnieuw getekend worden en de score ge reset
    begin_stukken(veld_grootte)
    teken_score()

def begin_stukken(veld_grootte):
    center = plaatje_size / 2
    teken_stuk(center, center, 1, True)
    teken_stuk(center-plaatje_size/veld_grootte, center, 2, True)
    teken_stuk(center, center-plaatje_size/veld_grootte, 2, True)
    teken_stuk(center-plaatje_size/veld_grootte, center-plaatje_size/veld_grootte, 1, True)

def omliggende_check(speler):
    # we gebruiken een set ipv een lijst omdat we geen dubbele waardes willen en sets sneller zijn dan lijsten
    # ook zijn er geen arrays in python :( https://i.pinimg.com/originals/90/04/68/90046863e1a4b223f13573e747199de3.gif
    lege_plaatsen = set()    
    andere_speler = speler
    speler = (speler)%2 +1
    
    delta = [-1, 0, 1, 0, -1, -1, 1, 1, -1] # de 8 richtingen lees als (-1,0) (0,1) (1,0) ect.
    grid_squared = grid_size**2
    for i in range(0,grid_squared):
        if lijst1[i] == speler:
            x,y = lijst_grid(i)
            for j in range(8): # per richting vanaf de gezette steen kijken we welke stukken er geslagen worden         
                dx, dy = delta[j], delta[j+1]
                # we kijken voor alle stenen van de huidige speler of er een steen van de andere speler om heen ligt
                if (x+dx and y+dy ) <= grid_size and (x+dx and y+dy) >= 0 and lijst1[(grid_lijst(x+dx,y+dy))] == andere_speler:
                    for k in range(1,grid_size):
                        new_x, new_y = x+k*dx, y+k*dy

                        if (new_x or new_y ) > grid_size or (new_x or new_y) < 0:
                            break
                        elif lijst1[grid_lijst(new_x, new_y)] == 0:
                            # als er een lege plek is dan voegen we die toe aan de set met legale zetten,
                            # we hebben immers al gekeken of er een steen van de andere speler omheen ligt
                            lege_plaatsen.add((new_x, new_y))
                            break 
    return lege_plaatsen

def teken_zetten(speler):
    #verwijderd de oude hints door er een groen vierkantje over te tekenen
    if vorige_zetten != []:
        for i in vorige_zetten:
            a=i[0]
            b=i[1]
            if lijst1[grid_lijst(a,b)] == 0:
                a,b = grid_scherm(a,b)
                a += offset//2
                b+= offset//2
                draw.rectangle((a, b, a+straal, b+straal), fill="green")
    # als er geen legale moves zijn, geeft hij een popup
    # we gebruiken speler 3 want die bestaat niet, en dus worden er geen zetten getekend en de oude hints verwijderd
    if omliggende_check(speler) == set() and speler!=3:
        popupmsg("geen zetten mogelijk, druk op beurt overslaan")
    # als er legale moves zijn, dan tekent deze functie die als rooie cirkels
    else: 
        for i in omliggende_check(speler):
            a,b = i
            vorige_zetten.append((a,b))
            a,b = grid_scherm(a,b)

            a += offset*4
            b += offset*4
            draw.ellipse(((a,b),(a+straal/5,b+straal/5)),outline="Red", width=5)
    
    # invalidate()
    global foto
    foto = ImageTk.PhotoImage(plaatje)
    afbeelding.configure(image=foto)

def stukken_veranderen(speler, x, y):
    andere_speler = speler % 2 + 1
    delta = [-1, 0, 1, 0, -1, -1, 1, 1, -1] # 8 richtingen wordt hetzelfde gelezen als bij omliggende_check
    for j in range(8): # per richting vanaf de gezette steen kijken we welke stukken er geslagen worden
        dx, dy = delta[j], delta[j+1]
        geslagen_stukken = []  # de stukken die geslagen worden die we kunnen doorgeven aan de fuctie die de stukken tekent
        # we kijken voor alle stenen van de huidige speler of er een steen van de andere speler om heen ligt
        if (x+dx and y+dy ) <= grid_size and (x+dx and y+dy) > 0 and lijst1[(grid_lijst(x+dx,y+dy))] == andere_speler:
            for k in range(1,grid_size):
                new_x, new_y = x+k*dx, y+k*dy # dan hoeven we ze niet voor elke voorwaarde opnieuw te berekenen
                nx, ny = x+(k+1)*dx, y+(k+1)*dy
                if (new_x or new_y) > grid_size or (new_x or new_y) <1 or lijst1[grid_lijst(new_x, new_y)] == 0:
                    break
                elif lijst1[grid_lijst(new_x, new_y)] == andere_speler: 
                    #de stenen van de andere kleur die in een richting tegen de gezette steen aanliggen worden onthouden, 
                    # mits de volgende stap in die richting binnen het speelveld valt, anders kijken we naar de volgende richting
                    if nx > grid_size or ny > grid_size or nx <1 or ny < 1 or lijst1[grid_lijst(nx,ny)]==0:
                        break 
                    else:
                        geslagen_stukken.append((new_x, new_y))
                elif lijst1[grid_lijst(new_x, new_y)] == speler:
                    #als de steen andere stenen insluit met een steen van de speler,
                    #dan worden die stenen verandert naar de stenen van de speler en gaan we door naar de volgende richting
                    for i in geslagen_stukken:
                        teken_stuk(*grid_scherm(i[0],i[1]), speler, computer = True, kut_recursie=False)
                        speler_lijst(*i,speler)
                    break     

def teken_stuk(x,y,speler, computer=False, kut_recursie=True):
    # tekent de stenen, als computer = True dan kunnen er "illegale" zetten worden gemaakt om bijv. 
    # de stenen te slaan of de begin stenen te plaatsen
    global beurt_speler
    
    x,y = snap_plaats(x,y)
    grid_x, grid_y = scherm_grid(x,y)
    
    #centreert de stukken
    x += offset//2
    y += offset//2  
    
    # checkt of de grid positie al bezet is
    if lijst1[grid_lijst(grid_x,grid_y)] != 0 and computer is False:
        return
    # checkt of de grid positie niet een legale zet is, en geen begin stuk is, die worden immers niet via legale zetten geplaatst
    if (grid_x,grid_y) not in [opties for opties in omliggende_check((speler%2+1))] and computer is False:
        print("niet mogelijk om hier te plaatsen")
        return
    # zorgt ervoor dat twee functies niet elkaar aanroepen
    if kut_recursie:
        stukken_veranderen(beurt_speler, grid_x, grid_y)
    speler_lijst(grid_x,grid_y,speler)
    # we hebben hier bepaald dat speler 1 = wit en speler 2 = zwart en deze worden hier getekend
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
    global bots_aan
    # als er geen legale zetten zijn voor beide spelers dan is het spel afgelopen
    if len(omliggende_check(speler)) == 0 and len(omliggende_check(speler%2+1)) == 0:
        teken_score()
        # geeft een popup met de winnaar
        popupmsg("gelijkspel :(" if lijst1.count(1)==lijst1.count(2)
                 else ("ZWART WINT!" if lijst1.count(1) <lijst1.count(2)
                 else "WIT WINT!"))
        
        bots_aan = False
        botvsbot_knop.config(text="bot vs bot")
        
        if lijst1.count(1) < lijst1.count(2): #als zwart meer stenen heeft dan wint zwart
            image = Image.open("Big_Black_Cock.jpeg")
            image.show()
        elif lijst1.count(2) < lijst1.count(1): #als wit meer stenen heeft wint wit
            image = Image.open("bwc.jpg")
            image.show()
        else: # anders is het gelijk spel
            image = Image.open("Screenshot1.png")
            image.show()

# voert een zet uit, waarbij de locatie van het stuk door de bot is gekozen
def bot_zet():
    global beurt_speler
    legale_plekken = omliggende_check(beurt_speler%2+1)
    if len(legale_plekken) == 0 :
        beurt_speler = beurt_speler%2+1
        return
    # kiest een willekeurige tupel uit legale_plekken, maar hier komen ook tupels in voor die geen legale zet zijn,
    # maar die filteren we er hier pas uit, omdat het anders rete traag was
    x, y = random.choice(list(legale_plekken))
    while x>grid_size or y>grid_size or x<1 or y<1:
        x, y = random.choice(list(legale_plekken))
    else:
        speel_een_beurt(grid_scherm(x,y)[0], grid_scherm(x,y)[1])
        
# laat de bot tegen zichzelf spelen
def bvb_thread():
    global beurt_speler
    while bots_aan:
        
        if len(omliggende_check(beurt_speler%2+1)) == 0:
            beurt_knop_klik()
        bot_zet()

        time.sleep(0.08)

# event handler voor de bot vs bot knop die een thread start/stopt waar de bot tegen zichzelf speelt
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
    
def speel_een_beurt(x,y):
    global beurt_speler, zetten_tekenen
    # omdat python sloom is gebruiken we multithreading
    t2 = threading.Thread(target=omliggende_check, args=(beurt_speler,)) 
    t2.start()
    teken_stuk(x,y,beurt_speler)
    zetten_tekenen = False # zorgt dat je niet 2 keer op hint moet klikken
    teken_zetten(3) # haalt de hints weg
    winner(beurt_speler) # checkt of er een winnaar is
    teken_score() # tekent de score
    
def muisKlik(ea):
    speel_een_beurt(ea.x,ea.y)
    
default = tk.StringVar(scherm)
# de default waarde van het speelveld en de opties voor de grootte van het speelveld
default.set("6x6")
opties = ["4x4","6x6", "8x8", "10x10", "20x20", "30x30"]
drop = tk.OptionMenu(scherm, default,*opties)
drop.place(x=0, y=620)
# alle knoppen
beurt_knop = tk.Button(scherm, text="beurt overslaan", command=beurt_knop_klik)
beurt_knop.place(x=650, y=30)
bot_knop = tk.Button(scherm, text="bot", command=bot_klik)
bot_knop.place(x=650, y=220)
botvsbot_knop = tk.Button(scherm, text="bot vs bot", command=bvb_klik)
botvsbot_knop.place(x=700, y=220)
nieuw_spel_knop = tk.Button(scherm, text="nieuw spel", command=lambda: lees_dropdown())
nieuw_spel_knop.place(x=80, y=620)
hulp_knop = tk.Button(scherm, text="help", command=hulp_knop_klik)
hulp_knop.place(x=650, y=60)

speelveld_tekenen(grid_size)
afbeelding.bind("<Button-1>", muisKlik)
scherm.mainloop()