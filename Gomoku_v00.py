import pygame
import numpy as np
pygame.init()
screen = pygame.display.set_mode((750,750)) # set screen size
pygame.display.set_caption("Gomoku1.0")

border_left = 25
boarder_right = 725
border_top = 25
boarder_bottom = 725
width = 50 
height = 50 

class Game:
    def __init__(self) -> None: # initial settings
        self.player = 1
        self.winner = 0
        self.map = np.zeros((15,15))

    def start(self): # start game setting
        screen.fill("#EE9A49") # set background color 
        for x in range(15):
            pygame.draw.line(screen, "#000000", [border_left+width*x,border_top],[border_left+width*x,boarder_bottom],2) # draw verticle lines 
            pygame.draw.line(screen, "#000000", [border_left,border_top+height*x],[boarder_right,border_top+height*x],2) # draw horizaontal lines
        pygame.draw.circle(screen, "#000000", [25+50*7,25+50*7], 8) # draw center circle
        ## user actions
        x,y = pygame.mouse.get_pos() # get mouse position
        x = round((x - border_left)/width)*width + border_left # more precise location 
        y = round((y - border_top)/height)*height + border_top
        pygame.draw.rect(screen, "#FFFFFF", [x-25,y-25,50,50],1) # draw mouse prompt
        for row in range(15):
            for col in range(15):
                if self.map[row,col] == 1:
                    pygame.draw.circle(screen, "#000000", [col*width+border_left,row*height+border_top], 25)
                elif self.map[row,col] == 2:
                    pygame.draw.circle(screen, "#FFFFFF", [col*width+border_left,row*height+border_top], 25)
        if(self.winner!=0):
            if self.winner == 1:
                text = 'black wins'
                color = (0,0,0)
            else:
                text = 'white wins'
                color = (255,255,255)
            font = pygame.font.Font(size=70)
            text_surface = font.render(text,True,color)
            text_position = (100,100)
            screen.blit(text_surface, text_position)
            pygame.display.update()

    def check(self,row,col): # check winning condition
        # decide whether there is FIR in L/R
        score = 1
        for i in range(4): # right 
            try:
                if self.map[row,col+i] == self.map[row,col+i+1]:
                    score = score + 1
                else:
                    break
            except:
                break
        for i in range(4): # left
            try:
                if self.map[row,col-i] == self.map[row,col-i-1]:
                    score = score + 1
                else:
                    break
            except:
                break
        if score >= 5:
            return True
        
        # decide whether there is FIR in U/D
        score = 1
        for i in range(4): # right 
            try:
                if self.map[row+i,col] == self.map[row+i+1,col]:
                    score = score + 1
                else:
                    break
            except:
                break
        for i in range(4): # left
            try:
                if self.map[row-i,col] == self.map[row-i-1,col]:
                    score = score + 1
                else:
                    break
            except:
                break
        if score >= 5:
            return True
        
        # decide whether there is FIR in LD/RU
        score = 1
        for i in range(4): # right 
            try:
                if self.map[row+i,col+i] == self.map[row+i+1,col+i+1]:
                    score = score + 1
                else:
                    break
            except:
                break
        for i in range(4): # left
            try:
                if self.map[row-i,col-i] == self.map[row-i-1,col-i-1]:
                    score = score + 1
                else:
                    break
            except:
                break
        if score >= 5:
            return True
        
        # decide whether there is FIR in LU/RD
        score = 1
        for i in range(4): # right 
            try:
                if self.map[row-i,col+i] == self.map[row-i-1,col+i+1]:
                    score = score + 1
                else:
                    break
            except:
                break
        for i in range(4): # left
            try:
                if self.map[row+i,col-i] == self.map[row+i+1,col-i-1]:
                    score = score + 1
                else:
                    break
            except:
                break
        if score >= 5:
            return True
        
    def mouseClick(self,x,y): # mouse click
        col = round((x - 25)/50) 
        row = round((y - 25)/50) 
        if self.map[row,col] == 0: # taken avoid double stones
            self.map[row,col] = self.player # alternative stones 
            if(self.check(row,col)):
                self.winner = self.player
            else:
                if self.player == 1:
                    self.player = 2
                else:
                    self.player = 1
        else:
            pass # do nothing

game = Game()

while True: # main 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos() # get mouse position
            game.mouseClick(x,y)
    game.start()
    pygame.display.update()