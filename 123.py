import turtle
import time

# Set up the screen
screen = turtle.Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")

# Create the turtle object
pen = turtle.Turtle()
pen.speed(0)
pen.color("pink")
pen.hideturtle()

# Draw heart incrementally
def draw_heart():
    pen.penup()
    pen.goto(0, -100)
    pen.pendown()

    # Start drawing the heart step by step
    pen.begin_fill()
    pen.fillcolor("pink")

    # Draw the left half of the heart
    pen.left(140)
    for _ in range(200):
        pen.forward(1)
        pen.left(1)
        screen.update()  # Update the screen
        time.sleep(0.01)  # Delay for animation

    pen.left(120)

    # Draw the right half of the heart
    for _ in range(200):
        pen.forward(1)
        pen.left(1)
        screen.update()  # Update the screen
        time.sleep(0.01)  # Delay for animation

    pen.end_fill()

# Update the screen at the start
screen.tracer(0)

# Draw the heart with animation
draw_heart()

# Keep the window open until closed
turtle.done()
