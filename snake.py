
""" Import Packages """
import turtle
import time
from random import random , randint
#from playsound import playsound
import requests
from turtle import Turtle, Screen
import pygame

""" Set up the sounds """
pygame.mixer.init()
pygame.mixer.music.load("snake_sound.mp3")

""" Webscrape Background, Game Over Sound and Food Image """
#background
url = 'https://github.com/RoelTim/snake-game/blob/master/background.gif?raw=true'
r = requests.get(url, allow_redirects=True)
open('background.gif', 'wb').write(r.content)

#food (target for the snake)
url='https://github.com/RoelTim/snake_game/blob/master/food.gif?raw=true'
r = requests.get(url, allow_redirects=True)
open('food.gif', 'wb').write(r.content)

""" Set Up the Screen """
wn = turtle.Screen()
wn.bgcolor("grey")
wn.title("Snake Game made by Roelien")
wn.bgpic('background.gif')
wn.update()
wn.setup(width=800, height=800)
wn.tracer(0) # Turns off the screen updates

""" Write the score and high score with a pen """
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("Score: 0  High Score: 0", align="center", font=("Courier", 24, "normal"))
score = 0
high_score = 0

""" Create the head of the Snake """
head = turtle.Turtle()
speed=0
head.speed(speed)
head.shape("square")
head.color("blue")
head.penup()
head.goto(0,0)
head.direction = "stop"
segments = []


""" Create 2 types of food for the Snake """
# Snake food
food1 = turtle.Turtle()
food1.speed(0)
wn.addshape('food.gif')
food1.shape('food.gif')
food1.color("red")
food1.penup()
food1.goto(0,100)

food2 = turtle.Turtle()
food2.speed(0)
food2.shape('food.gif')
food2.color("green")
food2.penup()
food2.goto(0,-100)

""" Set the delay """
delay = 0.1

""" Define all the functions"""

def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)

    if head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

""" Keyboard Bindings """
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

""" Main Game Loop"""
while True:
    wn.update()

    # Check for a collision with the border
    if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
        pygame.mixer.music.play()  
        time.sleep(2)
        head.goto(0,0)
        wn.update()
        
        for segment in segments:
            segment.goto(1000, 1000)# Hide the segments
        
        segments.clear() #Clear the segments list
        score = 0 #Reset the score
        delay = 0.1 #Reset the delay

        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

    # Check for a collision with the food1
    if head.distance(food1) < 20 or head.distance(food2) < 20:
        
        wn.update()
        if head.distance(food1) < 20: 
            food1.color(random(),random(),random())
            food1.goto(randint(-290, 290),randint(-290, 290))

        if head.distance(food2) < 20: 
            food2.color(random(),random(),random()) #create food with a random colour
            food2.goto(randint(-290, 290),randint(-290, 290))# Move the food2 to a random spot

        new_segment = turtle.Turtle() #create a new segment for the snake
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color(random(), random(), random())
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.001 # Shorten the delay
        score += 10 # Increase the score

        if score > high_score:
            high_score = score
        
        speed=speed+1
        head.speed(speed)
        
        pen.clear()
        pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal")) 

    # Move the end segments first in reverse order
    for index in range(len(segments)-1, 0, -1):
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()
        segments[index].goto(x, y)

    # Move segment 0 to where the head is
    if len(segments) > 0:
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()    

    # Check for head collision with the body segments
    for segment in segments:
        if segment.distance(head) < 20:
            pygame.mixer.music.play()
            time.sleep(2)
            head.goto(0,0)
            head.direction = "stop"
        
            for segment in segments:
                segment.goto(1000, 1000) # Hide the segments
        
            segments.clear()# Clear the segments list
            score = 0 # Reset the score
            delay = 0.1 # Reset the delay
        
            # Update the score display
            pen.clear()
            pen.write("Score: {}  High Score: {}".format(score, high_score), align="center", font=("Courier", 24, "normal"))

    time.sleep(delay)

wn.mainloop()