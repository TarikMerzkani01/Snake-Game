
##Tarik Merzkani merzk001
##5/6/2020

#///////////////////// hw13 \\\\\\\\\\\\\\\\\\\\\
import tkinter as tk
import random

#Extra Credit Done:
#(I)-No Direction Reversal
#(II)-Restarting Mid-game
#(III)-Variable Game Difficulty: Easy, Normal, and Hard difficulties which relate
#       to how fast the game is running.
#(IV)-Pausing the Game
#(VII)-Enemy Snakes Can Lose
#(VIII)-Your Own Idea (Extra Credit VIII): Added a Start Screen, not too complex
#       but a pleasant greeting to the player. In addition with a Pause screen,
#       including a block so players don't cheat and pause consecutively to play
#       more sharply and achieve higher scores



#==========================================
# Purpose: Creates an interface of a game which the user can interact with.
#          The game is the famous snake game, which objective is to make a
#          snake as large as it can be before it dies and, thus, ends the game
# Instance variables: self.win: Window created using tkinter method
#                     self.canvas: Canvas created in self.win using canvas method
#                     self.playing: Boolean representing if game is playing (snakes are moving)
#                                   or not (on title screen or game over screen)
#                     self.speed: Integer multiplier that determines how fast the game is running,
#                                 determines how many milliseconds each loop takes. Default value is 1
#                     self.enemyalive: Boolean which determines if the enemy snake is alive or not
#                     self.pause: Boolean representing if the game is paused or not
#                     self.pausetext: Text for the pause screen
#                     self.pauseblock: White screen at pause screen
#                     self.Snake: Snake object representing the player
#                     self.enemy: Snake object representing the enemy snake
#                     self.board: Canvas rectangle that displays the boundaries of the game
#                     self.pellet: Canvas Oval Object representing the food pellet
# Methods: __init__: Constructor method that initiates anything needed when the program is ran before
#                    calling the self.gameloop method. Sets up key bindings for setting difficulty,
#                    starting/restarting the game, and pausing. Assigns default values for instance variables
#                    Also draws start screen.
#          gamestart: Method that sets self.playing to True and starts the game by assigning and creating
#                     objects for the game to run, primarily creating snake objects, drawing the board, mapping
#                     the directional keys to call the movement functions, and creating the food pellet on the screen.
#          foodpellet: Method that creates a red circle at a random position in the board grid. Used for generating
#                      food pellets at the start of the game and after one is 'eaten' by a snake
#          gameloop: Method that contains all conditional actions and states to do depending on what phase or event
#                    happens when the program is running. This is the method that loops with recursional call
#                    self.canvas.after(). Thus, each call has to do different things regarding different states the
#                    program is in (whether start screen, pause screen, game over screen, playing, player dies, enemy
#                    snake dies, food pellet being eaten).
#          harddiff: Method that sets self.speed to 0.75, making time after each loop shorter and thus making the game
#                    run faster
#          normdiff: Method setting normal difficulty, assigning self.speed to default value.
#          easydiff: Method setting easy difficulty for game, assigning self.speed to larger value and thus making the game
#                    run slower.
#          pausing: Method called by the pause button (spacebar), which sets self.pause to True if it is initially
#                   False, or False when it is initially True; this only happens while game is in the playing state.
#==========================================

class SnakeGUI:
    def __init__(self):
        self.win = tk.Tk()
        self.canvas = tk.Canvas(self.win, width = 660, height = 660)
        self.canvas.pack()
        self.playing = False
        self.speed = 1
        self.pause = False
        self.enemyalive = True
        self.win.bind('<space>',self.pausing)
        self.win.bind('r',self.gamestart)
        self.win.bind('1',self.easydiff)
        self.win.bind('2',self.normdiff)
        self.win.bind('3',self.harddiff)
        self.canvas.create_text(330, 220, text='//////////////////////////////////////////////////////////', font = ("Ariel", 23))
        self.canvas.create_text(330, 270, text='Counter Snake: Reptile Offensive!', font = ("Ariel", 30))
        self.canvas.create_text(330, 330, text="Press 'R' to start!", font = ("Ariel", 23))
        self.canvas.create_text(330, 360, text="(Restart with 'R' anytime!)", font = ("Ariel", 18))
        self.canvas.create_text(330, 390, text='//////////////////////////////////////////////////////////', font = ("Ariel", 23))
        self.canvas.create_oval(315, 435, 345, 465, fill = 'red')
        for i in range(3):
            self.canvas.create_rectangle(110+i*30, 435, 140+i*30, 465, fill = 'green')
            self.canvas.create_rectangle(460+i*30, 435, 490+i*30, 465, fill = 'purple')
        self.gameloop()
    def gamestart(self, event):
        self.canvas.delete(tk.ALL)
        self.playing = True
        self.enemyalive = True
        self.Snake = (Snake(330, 330, 'green', self.canvas, False))
        self.enemy = (Snake(540, 540, 'purple', self.canvas, True))
        self.board = self.canvas.create_rectangle(30, 30, 630, 630)
        self.win.bind('<Down>',self.Snake.go_down)
        self.win.bind('<Up>',self.Snake.go_up)
        self.win.bind('<Right>',self.Snake.go_right)
        self.win.bind('<Left>',self.Snake.go_left)
        self.pellet = self.foodpellet()
    def foodpellet(self):
        xfood = 30*random.randint(1,20)
        yfood = 30*random.randint(1,20)
        pellet = self.canvas.create_oval(xfood, yfood, xfood+30, yfood+30, fill = 'red')
        return pellet
    def gameloop(self):
        if not self.pause:
            if self.playing:
                setconditions = Snake.move(self.Snake, self.pellet, self.enemy)
                if setconditions[0]:
                    self.pellet = self.foodpellet()
                if self.enemyalive:
                    enemyconditions = Snake.move(self.enemy, self.pellet, self.Snake)
                    if enemyconditions[1]:
                        for seg in self.enemy.segments:
                            self.canvas.delete(seg)
                        self.enemy.segments = []
                        self.enemyalive = False
                    if enemyconditions[0]:
                        self.pellet = self.foodpellet()
                    if enemyconditions[2]:
                        self.playing = False
                        self.canvas.create_text(250, 100, text='"Snake, respond to me!', font = ("Ariel", 20))
                        self.canvas.create_text(330, 140, text='Snake!? SNAAAAAAAAAAAKE!!"', font = ("Ariel", 20))
                        self.canvas.create_text(330, 300, text='You lost!', font = ("Ariel", 29))
                        self.canvas.create_text(330, 340, text='Score: '+str(len(self.Snake.segments)), font = ("Ariel", 24))
                        self.canvas.create_text(330, 400, text='Press R to restart!', font = ("Ariel", 20))
                if setconditions[1]:
                    self.playing = False
                    self.canvas.create_text(250, 100, text='"Snake, respond to me!', font = ("Ariel", 20))
                    self.canvas.create_text(330, 140, text='Snake!? SNAAAAAAAAAAAKE!!"', font = ("Ariel", 20))
                    self.canvas.create_text(330, 300, text='You lost!', font = ("Ariel", 29))
                    self.canvas.create_text(330, 340, text='Score: '+str(len(self.Snake.segments)), font = ("Ariel", 24))
                    self.canvas.create_text(330, 400, text='Press R to restart!', font = ("Ariel", 20))
            if not self.playing:
                self.canvas.create_text(330, 530, text='Set difficulty:', font = ("Ariel", 17))
                self.canvas.create_text(330, 560, text='1-Easy, 2-Normal, 3-Hard', font = ("Ariel", 15))
        self.canvas.after(int(100*self.speed), self.gameloop)
    def harddiff(self, event):
        if not self.playing:
            self.speed = 0.75
    def normdiff(self, event):
        if not self.playing:
            self.speed = 1
    def easydiff(self, event):
        if not self.playing:
            self.speed = 1.25
    def pausing(self, event):
        if self.playing and not self.pause:
            self.pause = True
            self.pauseblock = self.canvas.create_rectangle(30, 30, 630, 630, fill = 'white')
            self.pausetext = self.canvas.create_text(330, 330, text='Pause!', font = ("Ariel", 57))
        elif self.pause:
            self.pause = False
            self.canvas.delete(self.pausetext)
            self.canvas.delete(self.pauseblock)






            
#==========================================
# Purpose: Creates a Snake object, a series of continuously created and removed rectangles
#          providing the illusion of movement. Represents all functions of a 'Snake' in a 
#          typical Snake Game
# Instance variables: self.x: Represents current x-position of snake
#                     self.y: Represents current y-position of snake
#                     self.color: Represents color of the snake rectangle
#                     self.canvas: Canvas created in SnakeGUI
#                     self.snake: Single rectangle for snake's head
#                     self.segments: Series of created and removed rectangles forming the snake
#                     self.vx: Velocity in x-direction
#                     self.vy: Velocity in y-direction
#                     self.enemy: Boolean representing if snake is an enemy snake
# Methods: __init__: Assigns instance variables for Snake object
#           move:    Move function for all Snake objects. Different for player and
#                    enemy snake, and includes all actions such as growing when eating
#                    a food pellet, dying due to collision with border, with one's own segment
#                    or another snake's segment. Returns a tuple of three boolean values representing 
#                    if any of these events happened. This method is called in the gameloop method of
#                    SnakeGUI, and uses these boolean values to determine what state the game is in
#                    (Gameover, enemy dies and disappears, or pellet is eaten and the respective snake grows).
#                    Main function of movement is adding velocities to their respective coordinates. Values are
#                    different, again, whether it is the player or the enemy snake.
#           go_down: Changes velocity's in the x and y-directions to make the illusion the snake is going downwards
#           go_up:   Changes velocity's in the x and y-directions to make the illusion the snake is going upwards
#          go_right: Changes velocity's in the x and y-directions to make the illusion the snake is going to the right
#          go_left:  Changes velocity's in the x and y-directions to make the illusion the snake is going to the left
#         enemymove: Method for enemy snakes, which takes self and the food pellet's ID. Uses a flowchart tree of
#                    If-Else logic using the food pellet's position and the enemy snake's position to determine which
#                    of the directional methods in Snake to call. Also evaluates special cases (same coordinates in an axis,
#                    direction reversal conflict, analyzing distance from borders).
#==========================================
class Snake:
    def __init__(self, xpos, ypos, color, canvas, enemystate):
        self.x = xpos
        self.y = ypos
        self.color = color
        self.canvas = canvas
        self.snake = self.canvas.create_rectangle(self.x, self.y,
                                                  self.x+30, self.y+30,
                                                  fill = self.color)
        self.segments = [self.snake]
        self.vx = 30
        self.vy = 0
        self.enemy = enemystate
        if self.enemy:
            self.vx = 0
            self.vy = 0
    def move(self, pellet, other):
        if self.enemy:
            self.enemymove(pellet)
        self.x += self.vx
        self.y += self.vy
        eaten = None
        end = False
        enemykill = False
        for seg in self.segments:
            if self.segments != []:
                if self.x == self.canvas.coords(seg)[0] and self.y == self.canvas.coords(seg)[1]:
                    end = True
                    self.canvas.itemconfig(self.segments[0], fill= 'orange')
                    self.canvas.itemconfig(seg, fill= 'orange')
        for seg in other.segments:
            if other.segments != []:
                if self.x == self.canvas.coords(seg)[0] and self.y == self.canvas.coords(seg)[1]:
                    end = True
                    self.canvas.itemconfig(self.segments[0], fill= 'orange')
                    self.canvas.itemconfig(seg, fill= 'orange')
                    enemykill = True
        if self.x < 30 or self.x >= 630 or self.y < 30 or self.y >= 630:
            end = True
            self.canvas.itemconfig(self.segments[0], fill= 'orange')
        if not end:
            self.segments.insert(0, self.canvas.create_rectangle(self.x, self.y,
                                                      self.x+30, self.y+30,
                                                      fill = self.color))
            if self.x != self.canvas.coords(pellet)[0] or self.y != self.canvas.coords(pellet)[1]:
                self.canvas.delete(self.segments.pop())
                eaten = False
            else:
                self.canvas.delete(pellet)
                eaten = True
        return eaten, end, enemykill
    def go_down(self,event=0):
        if self.vx != 0 or self.vy != -30:
            self.vx = 0
            self.vy = 30
            return True
        return False
    def go_up(self,event=0):
        if self.vx != 0 or self.vy != 30:
            self.vx = 0
            self.vy = -30
            return True
        return False
    def go_right(self,event=0):
        if self.vx != -30 or self.vy != 0:
            self.vx = 30
            self.vy = 0
            return True
        return False
    def go_left(self,event=0):
        if self.vx != 30 or self.vy != 0:
            self.vx = -30
            self.vy = 0
            return True
        return False
    def enemymove(self, pellet):                #AI function with a flowchart of if-else logic
        if self.x < self.canvas.coords(pellet)[0]:        
            if not self.go_right():                             
                                                                
                if self.y < self.canvas.coords(pellet)[1]:          
                    self.go_down()                                     
                elif self.y == self.canvas.coords(pellet)[1]:       
                    if self.y+30 < 630:                                
                        self.go_down()
                    elif self.y-30 > 30:
                        self.go_up()
                else:                                                   
                    self.go_up()
        elif self.x == self.canvas.coords(pellet)[0]:       
            if self.y < self.canvas.coords(pellet)[1]:          
                if not self.go_down():                              
                    if self.x-30 > 0:                               
                        self.go_left()
                    elif self.x+30 < 630:
                        self.go_right()
            else:
                if not self.go_up():
                    if self.x-30 > 0:
                        self.go_left()
                    elif self.x+30 < 630:
                        self.go_right()
        else:
            if not self.go_left():
                if self.y < self.canvas.coords(pellet)[1]:
                    self.go_down()
                elif self.y == self.canvas.coords(pellet)[1]:       
                    if self.y+30 < 630:                               
                        self.go_down()
                    elif self.y-30 > 30:
                        self.go_up()
                else:
                    self.go_up()
        



SnakeGUI()
tk.mainloop()