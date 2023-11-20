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
        self.black_key = 1
        self.white_key = 2
        self.player = 1
        self.winner = 0
        self.map = np.zeros((15,15))

    def start(self): # start game setting
        yellow = "#EE9A49"
        black = "#000000"
        white = "#FFFFFF"
        screen.fill(yellow) # set background color 
        for x in range(15): # draw board lines
            pygame.draw.line(screen, black, [border_left+width*x,border_top],[border_left+width*x,boarder_bottom],2) # draw verticle lines 
            pygame.draw.line(screen, black, [border_left,border_top+height*x],[boarder_right,border_top+height*x],2) # draw horizaontal lines
        pygame.draw.circle(screen, black, [25+50*7,25+50*7], 8) # draw center circle
        ## user actions
        x,y = pygame.mouse.get_pos() # get mouse position
        x = round((x - border_left)/width)*width + border_left # more precise location 
        y = round((y - border_top)/height)*height + border_top
        pygame.draw.rect(screen, white, [x-25,y-25,50,50],1) # draw mouse prompt
        for row in range(15):
            for col in range(15):
                if self.map[row,col] == self.black_key: # black
                    pygame.draw.circle(screen, black, [col*width+border_left,row*height+border_top], 25)
                elif self.map[row,col] == self.white_key: # white
                    pygame.draw.circle(screen, white, [col*width+border_left,row*height+border_top], 25)
        if(self.winner!=0):
            if self.winner == self.black_key:
                text = 'Black Wins'
                color = (0,0,0)
            else:
                text = 'White Wins'
                color = (255,255,255)
            font = pygame.font.Font(size=70)
            text_surface = font.render(text,True,color)
            text_position = (100,100)
            screen.blit(text_surface, text_position)
            pygame.display.update()

    def check_consecutive(self,sequence, key):
        count = 0
        for element in sequence:
            if element == key:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0
        return False

    def check(self):
        # Check rows and columns
        for i in range(len(self.map)):
            if self.check_consecutive(self.map[i, :], self.black_key) \
                or self.check_consecutive(self.map[:, i], self.black_key) \
                    or self.check_consecutive(self.map[i, :], self.white_key) \
                        or self.check_consecutive(self.map[:, i], self.white_key):
                return True
        # Check main diagonals (top-left to bottom-right)
        for d in range(-len(self.map) + 1, len(self.map)):
            diagonal = np.diagonal(self.map, offset=d)
            if self.check_consecutive(diagonal, self.black_key) \
                or self.check_consecutive(diagonal, self.white_key):
                return True
        # Check anti-diagonals (top-right to bottom-left)
        for d in range(-len(self.map) + 1, len(self.map)):
            anti_diagonal = np.diagonal(np.fliplr(self.map), offset=d)
            if self.check_consecutive(anti_diagonal, self.black_key) \
                or self.check_consecutive(anti_diagonal, self.white_key):
                return True
        return False
    
    def mouseClick(self,x,y): # mouse click
        col = round((x - 25)/50) 
        row = round((y - 25)/50) 
        if self.map[row,col] == 0: # if the point is empty 
            self.map[row,col] = self.player # alternative stones 
            if(self.check()):
                self.winner = self.player
            else:
                if self.player == 1: # alternative
                    self.player = 2
                else:
                    self.player = 1
        else:
            pass # do nothing

    # def evaluateBoard(self):
    #     # Check rows and columns
    #     for i in range(len(self.map)):
    #         if self.check_consecutive(self.map[i, :], self.black_key) \
    #             or self.check_consecutive(self.map[:, i], self.black_key) \
    #                 or self.check_consecutive(self.map[i, :], self.white_key) \
    #                     or self.check_consecutive(self.map[:, i], self.white_key):
            

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