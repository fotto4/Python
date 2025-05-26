import turtle

# Fenster konfigurieren
wn = turtle.Screen()
wn.bgcolor("white")
wn.title("Schnell entstehendes Herz")

# Turtle konfigurieren
pen = turtle.Turtle()
pen.speed(2)  # Zeichengeschwindigkeit
pen.color("red")
pen.width(2)

# Funktion, um das Herz zu zeichnen
def draw_heart():
    pen.penup()
    pen.goto(0, -200)
    pen.pendown()
    pen.left(120)
    pen.begin_fill()

    # Linke Seite des Herzens
    for _ in range(200):
        pen.forward(2)
        pen.right(1)
    
    # Rechte Seite des Herzens
    pen.left(120)
    for _ in range(200):
        pen.forward(2)
        pen.right(1)
    
    pen.forward(225)
    pen.end_fill()

# Herz zeichnen
draw_heart()

# Animation stoppen
pen.hideturtle()
wn.mainloop()