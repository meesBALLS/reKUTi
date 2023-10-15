from tkinter       import Frame, Label, Button
import tkinter     as tk
import threading
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

scherm = Frame()
scherm.master.title("reKUTi")
scherm.configure(background="lightblue")
scherm.configure(width=scherm_size, height=scherm_size)
scherm.pack()


lijst1 = [(0)for i in range(0, grid_size**2)]

def knop1_klik():
    global beurt_speler
    beurt_speler = beurt_speler%2+1
    undraw_zetten()
    teken_score()


def knop2_klik():
    global zetten_tekenen
    global beurt_speler
    if not zetten_tekenen:
        zetten_tekenen = True
        teken_zetten(beurt_speler%2+1)
    else:  
        zetten_tekenen = False
        undraw_zetten()


# def text_score(speler):
#     score = lijst1.count(speler)
#     andere_score = lijst1.count(speler%2+1)
#     score_text.set("rood" if speler == 1 else "blauw" 'score:', score \
#     ,"blauw" if speler ==2 else "rood", andere_score)
    

# score_box = tk.Tk()
# score_text = tk.StringVar()
# score_text.set("blauw: 2, rood:2")

# tekst_label = tk.Label(score_box, textvariable=score_text, width=50, height=15)
# tekst_label.place(x=650, y=100)

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
    draw.rectangle((0, 0, plaatje_size, plaatje_size), fill="White")
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

canvas = tk.Canvas(scherm, width=200, height=20)
canvas.place(x=650, y=100)

blue_label = tk.Label(scherm, text="Blauw: 0", font=("Arial", 10))
blue_label.place(x=650, y=120)
red_label = tk.Label(scherm, text="Rood: 0", font=("Arial", 10))
red_label.place(x=750, y=120)

turn_label = tk.Label(scherm, text="Rood is aan de beurt", font=("Arial", 10))
turn_label.place(x=650, y=160)

plaatje = Image.new( mode="RGBA" , size=(plaatje_size,plaatje_size)) 
draw = Draw(plaatje)
afbeelding = Label(scherm) 
afbeelding.place(x=0, y=0) 
afbeelding.configure(width=plaatje_size, height=plaatje_size, bg="White")
afbeelding.configure(bg="white")

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
    if total_stones == 0:
        red_percentage = 0
    else:
        red_percentage = lijst1.count(1) / total_stones

    # draw the red and blue bars
    canvas.create_rectangle(0, 0, 200 * red_percentage, 20, fill="blue")
    canvas.create_rectangle(200 * red_percentage, 0, 200, 20, fill="red")
    blue_label.config(text=f"Blauw: {lijst1.count(1)}")
    red_label.config(text=f"Rood: {lijst1.count(2)}")
    turn_label.config(text=f"Rood is aan de beurt" if beurt_speler == 2 else f"Blauw is aan de beurt")
# score_box = tk.Tk()
# score_text = tk.StringVar()
# score_text.set("blauw: 2, rood:2")

# tekst_label = tk.Label(score_box, textvariable=score_text, width=50, height=15)
# tekst_label.place(x=650, y=100)




def speelveld_tekenen(veld_grootte):
    global plaatje_size
    lijn_pos = plaatje_size / veld_grootte
    #tekent de lijnen die het speelveld vormen
    for i in range(1,veld_grootte):
        draw.line(((lijn_pos*i,0),(lijn_pos*i,plaatje_size)),fill="black")
        draw.line(((0,lijn_pos*i),(plaatje_size,lijn_pos*i)),fill="black")
    
    begin_stukken(veld_grootte)
    teken_score()
    # teken_zetten(beurt_speler%2+1)

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
                            print("buiten kut")
                            break
                        elif lijst1[grid_lijst(new_x, new_y)] == speler:
                            break
                        elif lijst1[grid_lijst(new_x, new_y)] == 0:
                            lege_plaatsen.add((new_x, new_y))
                            break
    return lege_plaatsen

def undraw_zetten():
    if vorige_zetten != []:
        for i in vorige_zetten:
            a=i[0]
            b=i[1]
            if lijst1[grid_lijst(a,b)] == 0:
                a,b = grid_scherm(a,b)
                a += offset//2
                b+= offset//2
                draw.rectangle((a, b, a+straal, b+straal), fill="White")

def teken_zetten(speler):
    for i in omliggende_check(speler):
        a,b = i
        vorige_zetten.append((a,b))
        a,b = grid_scherm(a,b)

        a += offset*4
        b += offset*4
        draw.ellipse(((a,b),(a+straal/5,b+straal/5)),outline="Grey", width=5)
    
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
                if (new_x or new_y ) > grid_size or (new_x or new_y) <= 0 or lijst1[grid_lijst(new_x, new_y)] == 0:
                    print("buiten kut")
                    del geslagen_stukken[:-(k+1)]
                    break
                elif lijst1[grid_lijst(new_x, new_y)] == andere_speler:
                    if (x+(k+1)*dx or y+(k+1)*dy) > grid_size or (x+(k+1)*dx or y+(k+1)*dy) <= 0 and lijst1[grid_lijst(x+(k+1)*dx,y+(k+1)*dy)]!=0:
                        del geslagen_stukken[:-k]
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

    #
    x += offset//2
    y += offset//2  
    
    # checkt of de grid positie al bezet is
    if lijst1[grid_lijst(grid_x,grid_y)] != 0 and computer is not True:
        #print("niet mogelijk om hier te plaatsen")
        return

    if (grid_x,grid_y) not in [opties for opties in omliggende_check((speler%2+1))] and computer is False:
        print("niet mogelijk om hier te plaatsen")
        return
    if kut_recursie:
        stukken_veranderen(beurt_speler, grid_x, grid_y)
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
    undraw_zetten()
    teken_stuk(ea.x,ea.y,beurt_speler)
    t1 = threading.Thread(target=omliggende_check, args=(beurt_speler,))
    t1.start()
    t1.join()
    #omliggende_check(beurt_speler)
    if zetten_tekenen:
        teken_zetten(beurt_speler%2+1)
   
    if lijst1.count(1) == 0 or lijst1.count(1)+lijst1.count(2)==grid_size**2 and lijst1.count(2)>grid_size**2/2:
        popupmsg("rood wint")
    elif lijst1.count(2) ==0 or lijst1.count(1)+lijst1.count(2)==grid_size**2:
        popupmsg("blauw wint")
    print(f"aantal stenen {'blauw' if beurt_speler ==1 else 'rood'}",lijst1.count(beurt_speler))
    print(f"aantal stenen {'blauw' if beurt_speler ==2 else 'rood'}",lijst1.count(beurt_speler%2+1))
    teken_score()
    
    

# een Label kan ook gebruikt worden om een PhotoImage te laten zien
knop1 = Button(scherm, text="beurt overslaan", command=knop1_klik)
knop1.place(x=650, y=30)
knop2 = Button(scherm, text="hint", command=knop2_klik)
knop2.place(x=650, y=60)
speelveld_tekenen(grid_size)
afbeelding.bind("<Button-1>", muisKlik)
scherm.mainloop()

