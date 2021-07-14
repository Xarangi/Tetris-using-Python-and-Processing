import random
WIDTH=200
HEIGHT=400
rows=HEIGHT/20
cols=WIDTH/20

def setup(): #sets up the window
    size(WIDTH,HEIGHT)
def draw():
#slow down the game by not displaying every frame
    if frameCount%(max(1, int(8 - game.speed)))==0 or frameCount==1:
        background(210)
        if game.game==0:     #prints the starting screen
            fill(0,0,0)
            textSize(30)
            text('TETRIS RUSH',WIDTH*1/20,HEIGHT*2/5)
            textSize(15)
            text('Click to start ',WIDTH*2/7,HEIGHT*4/7)
            
        if game.replay==1:   #resets all the attributes of the game class
            game.block=[]
            game.i=0
            game.listx=[]
            game.replay=0
            game.block.append(Block())
            for r in range(rows):    #resets matrix
                for c in range(cols):
                    game.matrix[r][c]=''
            game.score=0
            game.speed=0
            
        if len(game.block)>rows*cols-1: #prints the Game Over screen along with the final score
           background(210)
           textSize(15)
           text('FINAL SCORE: '+str(game.score),WIDTH*1/4,HEIGHT*4/7)
           textSize(30)
           text('GAME OVER',WIDTH*1/10,HEIGHT*2/5)
           textSize(15)
           text('Click to restart ',WIDTH*1/4,HEIGHT*6/7)
           
        else: 
            #this calls the display method of the game class
            if game.game==1:
                game.display()
                strokeWeight(1)
                stroke(180)
                for c in range(rows+1):
                    for d in range(cols+1):
                        line(d*20,0,d*20,c*20)
                        line(0,c*20,d*20,c*20)
                fill(0,0,0)
                textSize(15)
                #this displays the score
                text('SCORE: '+str(game.score),WIDTH*1/2,HEIGHT*1/8)
#the following functions help us track the button we click on our keyboard, pressing left will move our block one column to the left and pressing righ will move it to the right
def keyPressed():
    if keyCode == LEFT:
        game.block[game.i].key_handler[LEFT] = True
    elif keyCode == RIGHT:
        game.block[game.i].key_handler[RIGHT] = True
        
def keyReleased():
    if keyCode == LEFT:
        game.block[game.i].key_handler[LEFT] = False
    elif keyCode == RIGHT:
        game.block[game.i].key_handler[RIGHT] = False
        
#tracking the click of the mouse to start/restart the game
def mouseClicked():
    game.game=1
    if len(game.block)>rows*cols-1:
        game.replay=1
    
#block class contains the properties of the block
class Block:
    def __init__(self):
        #list_colors contains the codes of the colors of which we select one randomly
        self.list_colors=[[255,51,52,'R'],[12,150,228,'B'],[30,183,66,'G'],[246,187,0,'Y'],[76,0,153,'P'],[255,255,255,'W'],[0,0,0,'Bl']]
        self.color=random.randint(0,6)
        #choosing a random column to spawn our new block and setting the initial value of row to 0
        self.rand_col=random.randint(0,cols-1)
        self.r=0
        #key handler holds key-value pairs to help control our block's horizontal movement
        self.key_handler={LEFT:False,RIGHT:False}
        self.check=True # checks if our block can go down further
    def display(self):
        fill(self.list_colors[self.color][0],self.list_colors[self.color][1],self.list_colors[self.color][2])   #colors the block
        rect(self.rand_col*20,self.r*20,20,20) #draw the block
        self.update()
    def update(self):
        #the following block of code maps the left and right buttons on our keyboard to the left and right movement of the block and moves the block one row down everytime it is called
        if self.key_handler[LEFT] == True and self.rand_col>=1 and game.matrix[self.r][self.rand_col-1]=='' and self.check==True:
            self.rand_col+= -1
        elif self.key_handler[RIGHT] == True and self.rand_col<=cols-2 and game.matrix[self.r][self.rand_col+1]=='' and self.check==True:
            self.rand_col += 1
        if self.r<=rows-2 and game.matrix[self.r+1][self.rand_col]=="":
            self.r+=1
        else:
            game.matrix[self.r][self.rand_col]=self.list_colors[self.color][3] #the color code of the landed block is added to the same position in our matrix to help us check for a 4 block pair later
            self.check=False
            
#game class contains the properties of our game
class Game:
    def __init__(self):
        self.matrix=[]       #this 2d list will help us check if a certain row or column is occupied
        self.i=0             #this will keep track of how many blocks are presently visible on the screen
        for r in range(rows):    
            new_line=[]
            for c in range(cols):
                new_line.append('')
            self.matrix.append(new_line)
        self.replay=0      #initialised as 0, we turn it to 1 when we get game over, to decide when our program can restart
        self.listx=[]      #stores the column number of a block which lands on the top row, to prevent our program from  overwriting it
        self.game=0        #turns to 1 when we start our game for the first time
        self.speed=0       #gets incremented by 0.25 everytime a block lands, controls the frames per seconf of our program
        self.block=[]      #list which stores the blocks we create
        self.block.append(Block())       #appending the first block to our list
        self.score=0                     #stores the score
        
    def new_block(self):                                      #function to add a new block
        self.block.append(Block())
        while self.block[self.i].rand_col in self.listx:           #if a block occupies the top row of a particular column and our new block is initialised to the same row, we remove the new block and append another block
            self.block.remove(self.block[self.i])
            self.block.append(Block())
            
    def check(self): #function to check if we have a 4 block pair
        if  self.matrix[self.block[self.i].r][self.block[self.i].rand_col]==self.matrix[self.block[self.i].r+1][self.block[self.i].rand_col]==self.matrix[self.block[self.i].r+2][self.block[self.i].rand_col]==self.matrix[self.block[self.i].r+3][self.block[self.i].rand_col]:
            
            self.matrix[self.block[self.i].r][self.block[self.i].rand_col]=''                   #if a 4 block pair is found, the corresponding positions in the matrix are cleared
            self.matrix[self.block[self.i].r+1][self.block[self.i].rand_col]=''
            self.matrix[self.block[self.i].r+2][self.block[self.i].rand_col]=''
            self.matrix[self.block[self.i].r+3][self.block[self.i].rand_col]=''

            if self.block[self.i].r==0:                                               #since we add every block in the top row to listx we have to remove the block form listx too if a 4 block pair is found
                self.listx.remove(self.block[self.i].rand_col)
            for x in range(rows):                                                #the blocks are removed from our list of blocks
                for s in range(cols):
                    for j in self.block:
                        if j.rand_col==s and j.r==x and self.matrix[x][s]=='':
                            self.block.remove(j)
                            
            self.i-=4                                                                 
            self.speed=0                                                         #speed is reset to 0
            self.score+=1                                                        #one point is added to our score
            
    def display(self):
        if self.game==1:
            for t in self.block:                                                 #all blocks in the list are displayed every time the for loop is run
                t.display()
            if t.check==False:                                                   #if the last block in the list has landed on a position, we increment the speed and append a new block
                self.speed+=0.25
                if t.r==0:                                                       #if it has landed on the top row, its column is added to listx
                    self.listx.append(t.rand_col)
                if t.r<=rows-4:                                                  #we call the check function when its possible to have a 4 block pair
                    self.check()
                self.i+=1
                self.new_block()
            
                

game=Game() #we create an object of the game class
