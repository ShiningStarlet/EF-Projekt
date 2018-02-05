# Libraries
import tkinter, random, time, _thread

# Start-Funktionen   
def start():
    global vx, vy, x_real, y_real, canvas, ball, seite_user, seite_pc, h, w, \
    restartbutton, punktestand, obstacle, label_punkte
    try:
        b_start.destroy()
        lb_regeln.destroy()
    except:
        pass
    text_punkte = "Punktestand: " + str(punktestand)
    label_punkte = tkinter.Label(main, height = 2, width = 50, anchor = "center",
                                 text = text_punkte, font = schrift,
                                 background = "white", relief = "ridge")
    canvas = tkinter.Canvas(main, height = h, width = w,
                            background = "black")
    seite_pc = canvas.create_rectangle(10, 50, 25, 125, fill = "green")
    seite_user = canvas.create_rectangle(w-25, 50, w-10, 125, fill = "green")
    ball = canvas.create_oval(100, 90, 125, 115, fill = "green")
    label_punkte.place(relx = 0.5, y = h+50, anchor = "n")
    canvas.place(relx = 0.5, y = 25, anchor = "n")
    canvas.bind("<Up>", rauf)
    canvas.bind("<Down>", runter)
    canvas.focus_set()
    if punktestand > 4:
        vx = random.randint(5, 11)/4
        vy = (4**2 - int(vx)**2)**0.5
        i = 3
    else:
        vx = random.randint(4, 10)/4
        vy = (3**2 - int(vx)**2)**0.5
        i = punktestand - 1
    x_real = 100
    y_real = 90
    obstacle = []
    for i in range(0, i):
        xo = random.randint(130, w - 100)
        yo = random.randint(0, h - 50)
        obstacle.append(canvas.create_rectangle(xo, yo, xo+15, yo+50,
                                                fill = "green"))
    _thread.start_new_thread(move_ball,())
    _thread.start_new_thread(eval_bally,())
    _thread.start_new_thread(eval_ballx,())
    _thread.start_new_thread(move_comp,())

def restart():
    global label_punkte, lb_abc, restartbutton, punktestand
    main.bind("<Return>", ignore)
    label_punkte.destroy()
    lb_abc.destroy()
    restartbutton.destroy()
    punktestand = 0
    start()

def restart_by_enter(e):
    restart()   # separate Funktion, weil beim Drücken der
                # Entertaste eine Funktion mit einem Parameter aufgerufen wird

# Funktion für Endbildschirm  
def ende():
    global canvas, punktestand, lb_abc, restartbutton, label_punkte
    canvas.destroy()
    label_punkte.place(relx = 0.5, y = h-150, anchor = "n")
    lb_abc = tkinter.Label(main, background = "white",
                           text = "Du bist am Ende des Spiels angekommen!",
                           font = "Arial 20 bold")   
    restartbutton = tkinter.Button(main, text = "Neuer Versuch",
                                   font = schrift, command = restart)
    lb_abc.place(relx = 0.5, rely = 0.3, anchor = "s")
    restartbutton.place(relx = 0.5, y = h+75, anchor = "s", width = 150)
    main.bind("<Return>", restart_by_enter)

# Funktion zum Bewegen des linken Balkens
def move_comp():
    global canvas, ball, seite_pc, x_real
    try:
        while x_real >= 1 and (x_real+15) <= (w-1):
            xu1, yu1, xu2, yu2 = canvas.coords(seite_user)
            xb1, yb1, xb2, yb2 = canvas.coords(ball)
            xp1, yp1, xp2, yp2 = canvas.coords(seite_pc)
            stoerfaktor = random.randint(1, 100)
            if yb1 > yp1 and stoerfaktor < 99:
                yp1 += 5
                yp2 += 5
                canvas.coords(seite_pc, xp1, yp1, xp2, yp2)
                time.sleep(0.05)
            elif yb1 < yp1 and stoerfaktor < 99:
                yp1 -= 5
                yp2 -= 5
                canvas.coords(seite_pc, xp1, yp1, xp2, yp2)
                time.sleep(0.05)
            else:
                for i in range (1, 3):
                    yp1 += 5
                    yp2 += 5
                    canvas.coords(seite_pc, xp1, yp1, xp2, yp2)
                    time.sleep(0.05)
    except:
        pass

# Funktion um den Ball zu bewegen
def move_ball():
    global vx, vy, x_real, y_real, canvas, ball
    while x_real >= 1 and (x_real+15) <= (w-1):
        time.sleep(0.001)
        x_real += vx
        y_real += vy
        canvas.coords(ball, int(x_real), int(y_real), int(x_real)+15, int(y_real)+15)

# Funktionen um die Position des Balles zu prüfen    
def eval_ballx():
    global vx, x_real, y_real, canvas, ball, obstacle
    while x_real >= 1 and (x_real+15) <= (w-1):
        x1, y1, x2, y2 = canvas.coords(seite_pc)
        if abs(x_real-x2)<1.5 and ((y1<y_real<y2) or (y1<(y_real+15)<y2)):
            vx *= -1
            time.sleep(0.15)
        x1, y1, x2, y2 = canvas.coords(seite_user)
        if abs(x1-(x_real+15)) < 1.5 and ((y1<y_real<y2) or (y1<(y_real+15)<y2)):
            vx *= -1
            time.sleep(0.15)
        for o in obstacle:
            x1, y1, x2, y2 = canvas.coords(o)
            if (abs(x1-(x_real+15)) < 1 or abs(x_real-x2) < 1) and \
                            ((y1<y_real<y2) or (y1<(y_real+15)<y2)):
                vx *= -1
                time.sleep(0.2)
        time.sleep(0.001)
    if x_real <= 1:
        frage_stellen()
    if (x_real+15) >= (w-1):
        ende()
    
def eval_bally():
    global vx, vy, x_real, y_real, canvas, ball, obstacle, seite_user
    while x_real >= 1 and (x_real+15) <= (w-1):
        if y_real <= 1 or (y_real+15) >= (h-1):
            vy *= -1
            time.sleep(0.15)
        x1, y1, x2, y2 = canvas.coords(seite_user)
        if (abs(y1-(y_real+15)) < 1.5 or abs(y2-y_real) < 1.5) and \
                            ((x1<x_real<x2) or (x1<(x_real+15)<x2)):
            vy *= -1
            time.sleep(0.15)
        x1, y1, x2, y2 = canvas.coords(seite_pc)
        if (abs(y1-(y_real+15)) < 1.5 or abs(y2-y_real) < 1.5) and \
                            ((x1<x_real<x2) or (x1<(x_real+15)<x2)):
            vy *= -1
            time.sleep(0.15)
        for o in obstacle:
            x1, y1, x2, y2 = canvas.coords(o)
            if (abs(y1-(y_real+15)) < 1.5 or abs(y2-y_real) < 1.5) and \
                                 ((x1<x_real<x2) or (x1<(x_real+15)<x2)):
                vy *= -1
                time.sleep(0.15)
        time.sleep(0.001)

# Funktionen für den Quizteil des Spiels      
def countdown():
    global label_antwort, label_frage
    label_countdown = tkinter.Label(main, font = schrift,
                                    background = "white")
    label_countdown.place(relx = 0.5, rely = 0.8, anchor = "n")
    t = 5
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        label_countdown["text"] = timeformat
        time.sleep(1)
        t -= 1
    label_countdown.destroy()
    label_antwort.destroy()
    label_frage.destroy()
    main.bind("<Left>", ignore)
    main.bind("<Right>", ignore)
    start()

def frage_stellen():
    global label_frage, label_antwort, nr, label_punkte                                     
    canvas.destroy()
    label_punkte.destroy()
    nr = random.randint(1,15)
    label_frage = tkinter.Label(main, text = fragen[nr], font = schrift,
                                background = "white", wraplength = 625,
                                height = 2, width = 55, anchor = "center")
    label_antwort = tkinter.Label(main, text = antwort[nr], font = schrift,
                                  background = "white", height = 2, width = 55,
                                  anchor = "center")
    label_frage.place(relx = 0.5, rely = 0.1, anchor = "n")
    label_antwort.place(relx = 0.5, rely = 0.4, anchor = "n")
    _thread.start_new_thread(countdown, ())
    label_antwort.bind("<Left>", links)
    label_antwort.bind("<Right>", rechts)
    label_antwort.focus_set()

# Funktionen für Tastenereignisse                                          
def rauf(e):
    global canvas, seite_user
    a, b, c, d = canvas.coords(seite_user)
    if b >= 10:
        canvas.move(seite_user, 0, -10)
    
def runter(e):
    global canvas, seite_user, h
    a, b, c, d = canvas.coords(seite_user)
    if (h-d) >= 0:
        canvas.move(seite_user, 0, +10)
    
def rechts(e):
    global nr, label_antwort, punktestand, label_frage
    if nr == 1 or nr == 5 or nr == 6 or nr == 8 or nr == 10 or nr == 14 or nr == 15:
        punktestand = punktestand + 1
        label_antwort["background"] = "green"
    else:
        label_antwort["background"] = "red"    
                                          
def links(e):
    global nr, label_antwort, punktestand
    if nr == 2 or nr == 3 or nr == 4 or nr == 7 or nr == 9 or nr == 11 or nr == 12 or nr == 13:
        punktestand = punktestand + 1
        label_antwort["background"] = "green"
    else:
        label_antwort["background"] = "red"

def ignore(e):
    pass # Funktion um Tastenereignisse zu blockieren
               
# Variablen
punktestand = 0
h = 500
w = 625
schrift = "Arial 14"

# Dictionary für Fragen
fragen = {}
fragen[1] = "Wieviele Einwohner hat die Schweiz?"
fragen[2] = "Wieviele Quadratkilometer Fläche hat die Schweiz?"
fragen[3] = "Wieviele Nationalräte hat der Kanton Tessin?"
fragen[4] = "Welche Sprache gehört zu den Landessprachen der Schweiz?"
fragen[5] = "Welches ist der grösste Schweizer See?"
fragen[6] = "In welchem Kanton liegt der geographische Mittelpunkt der Schweiz?"
fragen[7] = "Welches ist der längste Fluss, der durch die Schweiz fliesst?"
fragen[8] = "Welchem Tier ähnelt die Schweiz?"
fragen[9] = "Wo sagt man Himmugüägäli?"
fragen[10] = "Wie viele Mitglieder aus der Deutschschweiz hat der Bundesrat? (Stand August 17)"
fragen[11] = "Wann ist der Nationalfeiertag von Frankreich?"
fragen[12] = "Wer ist der Präsident von Deutschland?"
fragen[13] = "Welches ist die grösste Stadt Deutschlands?"
fragen[14] = "Pizza ist das Nationalgericht von ..."
fragen[15] = "Die A1 verläuft von ... nach ..."
# Dictionary für Antworten
antwort = {}
antwort[1] = "6 MILLIONEN    oder    8 MILLIONEN"
antwort[2] = "41000    oder    410000"
antwort[3] = "8    oder    18"
antwort[4] = "ITALIENISCH    oder    SCHWEIZERDEUTSCH"
antwort[5] = "NEUENBURGERSEE    oder    GENFERSEE"
antwort[6] = "URI    oder    OBWALDEN"
antwort[7] = "RHEIN    oder     RHONE"
antwort[8] = "SEEPFERD    oder    SCHILDKRÖTE"
antwort[9] = "BERN    oder    THURGAU"
antwort[10] = "4    oder    5"
antwort[11] = "14.07.    oder    01.08."
antwort[12] = "STEINMEIER    oder    TRUMP"
antwort[13] = "BERLIN    oder    BASEL"
antwort[14] = "ROM    oder    ITALIEN"
antwort[15] = "BERN - ZÜRICH    oder GENF - ST.GALLEN"

# Startbildschirm
main = tkinter.Tk()
main.configure(background='white')
main.geometry('%dx%d+%d+%d' % (w+50, h+125, 50, 0))
main.resizable(width = False, height = False)
spielregeln = "Welcome to Pong by Judith, Philine and Livia. Versuche mit deinem Brett (rechts) den Ball immer abzufangen. Mit den Pfeiltasten kannst du dein Brett nach oben und unten bewegen. Dein Ziel ist es, ihn ins Tor deines Gegenspielers zu befördern. Schaffst du das, wird eine Frage gestellt. Zwei Antworten sind möglich. Wenn die rechte Antwort die richtige ist, drücke die rechte Pfeiltaste; wenn die linke die richtige Antwort ist, drücke die linke Pfeiltaste. Den Punkt erhältst du nur, falls die Frage richtig beantwortet wird."
lb_regeln = tkinter.Label(main, text = spielregeln, wraplength = 450,
                          justify = "left", background = 'white',
                          font = "Arial 12")
b_start = tkinter.Button(main, text = "Start", command = start, font = schrift)
lb_regeln.place(relx = 0.5, rely = 0.5, anchor = "s")
b_start.place(relx = 0.5, y = h+75, anchor = "s", width = 100)

main.mainloop()
