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
        self.white_key = -1
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
        text = 'Board Score:'+str(self.BoardScore())
        color = (255,0,0)
        font = pygame.font.Font(size=30)
        text_surface = font.render(text,True,color)
        text_position = (10,6)
        screen.blit(text_surface, text_position)
        pygame.display.update()
        if(self.winner!=0):
            if self.winner == self.black_key:
                text = 'Black Wins'
                color = (0,0,0)
            else:
                text = 'White Wins'
                color = (255,255,255)
            font = pygame.font.Font(size=30)
            text_surface = font.render(text,True,color)
            text_position = (200,6)
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
                if self.player == self.black_key: # alternative
                    self.player = self.white_key
                else:
                    self.player = self.black_key
        else:
            pass # do nothing

    def BoardScore(self): # input a row/col/diag in self.map return scores
        scoreTotal = 0 

        def pattFreq(son, mother): # return pattern counter 
            counter = 0
            for i in range(len(mother)-len(son)): 
                if np.array_equal(son,mother[i:i+len(son)]):
                    counter += 1
            return counter
        
        def FiveInRow(arr): # return pattern freq
            patternBlackLib = np.array([1,1,1,1,1])
            patternWhiteLib = -patternBlackLib
            return [pattFreq(patternBlackLib,arr), pattFreq(patternWhiteLib,arr)]

        def LiveFour(arr):
            patternBlackLib = np.array([0,1,1,1,1,0])
            patternWhiteLib = -patternBlackLib
            return [pattFreq(patternBlackLib,arr), pattFreq(patternWhiteLib,arr)]
        
        def DeadFour(arr):
            blackFreq = 0 
            whiteFreq = 0
            patternBlackLib1 = np.zeros((2,6))
            patternBlackLib2 = np.zeros((3,5))
            patternBlackLib1[0,:] = np.array([0,1,1,1,1,-1])
            patternBlackLib1[1,:] = np.array([-1,1,1,1,1,0])
            patternBlackLib2[0,:] = np.array([1,0,1,1,1])
            patternBlackLib2[1,:] = np.array([1,1,1,0,1])
            patternBlackLib2[2,:] = np.array([1,1,0,1,1])
            patternWhiteLib1 = -patternBlackLib1
            patternWhiteLib2 = -patternBlackLib2
            for i in range(2):
                blackFreq += pattFreq(patternBlackLib1[i,:],arr)
                whiteFreq += pattFreq(patternWhiteLib1[i,:],arr)
            for i in range(3):
                blackFreq += pattFreq(patternBlackLib2[i,:],arr)
                whiteFreq += pattFreq(patternWhiteLib2[i,:],arr)
            return [blackFreq, whiteFreq]
        
        def LiveThree(arr):
            blackFreq = 0 
            whiteFreq = 0
            patternBlackLib1 = np.array([0,1,1,1,0])
            patternBlackLib2 = np.zeros([2,6])
            patternBlackLib2[0,:] = np.array([0,1,0,1,1,0])
            patternBlackLib2[1,:] = np.array([0,1,1,0,1,0])
            patternWhiteLib1 = -patternBlackLib1
            patternWhiteLib2 = -patternBlackLib2
            for i in range(2):
                blackFreq += pattFreq(patternBlackLib2[i,:],arr)
                whiteFreq += pattFreq(patternWhiteLib2[i,:],arr)
            blackFreq += pattFreq(patternBlackLib1,arr)
            whiteFreq += pattFreq(patternWhiteLib1,arr)
            return [blackFreq, whiteFreq]
            
        def DeadThree(arr):
            blackFreq = 0 
            whiteFreq = 0
            patternBlackLib1 = np.zeros((7,5))
            patternBlackLib2 = np.zeros((2,6))
            patternBlackLib3 = np.array([-1,0,1,1,1,0,-1])
            patternBlackLib1[0,:] = np.array([0,1,1,1,-1])
            patternBlackLib1[1,:] = np.array([-1,1,1,1,0])
            patternBlackLib1[2,:] = np.array([1,0,1,1,-1])
            patternBlackLib1[3,:] = np.array([-1,1,1,0,1])
            patternBlackLib1[4,:] = np.array([1,0,0,1,1])
            patternBlackLib1[5,:] = np.array([1,1,0,0,1])
            patternBlackLib1[6,:] = np.array([1,0,1,0,1])
            patternBlackLib2[0,:] = np.array([0,1,1,0,1,-1])
            patternBlackLib2[1,:] = np.array([-1,1,0,1,1,0])
            patternWhiteLib1 = -patternBlackLib1
            patternWhiteLib2 = -patternBlackLib2
            patternWhiteLib3 = -patternBlackLib3
            for i in range(2):
                blackFreq += pattFreq(patternBlackLib2[i,:],arr)
                whiteFreq += pattFreq(patternWhiteLib2[i,:],arr)
            for i in range(7):
                blackFreq += pattFreq(patternBlackLib1[i,:],arr)
                whiteFreq += pattFreq(patternWhiteLib1[i,:],arr)
            blackFreq += pattFreq(patternBlackLib3,arr)
            whiteFreq += pattFreq(patternWhiteLib3,arr)
            return [blackFreq, whiteFreq]
            
        def LiveTwo(arr):
            blackFreq = 0 
            whiteFreq = 0
            patternBlackLib1 = np.array([0,1,1,0])
            patternBlackLib2 = np.array([0,1,0,0,0,1,0])
            patternBlackLib3 = np.array([0,1,0,1,0])
            patternBlackLib4 = np.array([0,1,0,0,1,0])
            patternWhiteLib1 = -patternBlackLib1
            patternWhiteLib2 = -patternBlackLib2
            patternWhiteLib3 = -patternBlackLib3
            patternWhiteLib4 = -patternBlackLib4
            blackFreq = pattFreq(patternBlackLib1,arr) + pattFreq(patternBlackLib2,arr) \
                + pattFreq(patternBlackLib3,arr) + pattFreq(patternBlackLib4,arr)
            whiteFreq = pattFreq(patternWhiteLib1,arr) + pattFreq(patternWhiteLib2,arr) \
                + pattFreq(patternWhiteLib3,arr) + pattFreq(patternWhiteLib4,arr)
            return [blackFreq, whiteFreq]

        def DeadTwo(arr):
            blackFreq = 0 
            whiteFreq = 0
            patternBlackLib1 = np.zeros((2,4))
            patternBlackLib2 = np.zeros((2,5))
            patternBlackLib3 = np.zeros((2,6))
            patternBlackLib1[0,:] = np.array([0,1,1,-1])
            patternBlackLib1[1,:] = np.array([-1,1,1,0])
            patternBlackLib2[0,:] = np.array([0,1,0,1,-1])
            patternBlackLib2[1,:] = np.array([-1,1,0,1,0])
            patternBlackLib3[0,:] = np.array([0,1,0,0,1,-1])
            patternBlackLib3[1,:] = np.array([-1,1,0,0,1,0])
            patternWhiteLib1 = -patternBlackLib1
            patternWhiteLib2 = -patternBlackLib2
            patternWhiteLib3 = -patternBlackLib3
            for i in range(2):
                blackFreq += pattFreq(patternBlackLib1[i,:],arr)
                whiteFreq += pattFreq(patternWhiteLib1[i,:],arr)
                blackFreq += pattFreq(patternBlackLib2[i,:],arr)
                whiteFreq += pattFreq(patternWhiteLib2[i,:],arr)
                blackFreq += pattFreq(patternBlackLib3[i,:],arr)
                whiteFreq += pattFreq(patternWhiteLib3[i,:],arr)
            return [blackFreq, whiteFreq]

        blackFreqStats = np.zeros(7) # store pattern stats 
        whiteFreqStats = np.zeros(7)
        for i in range(len(self.map)): # get total frequency statistics for row and col 
            row = self.map[i,:]
            col = self.map[:,i]
            blackFreqStats[0] += FiveInRow(row)[0] + FiveInRow(col)[0]
            blackFreqStats[1] += LiveFour(row)[0] + LiveFour(col)[0]
            blackFreqStats[2] += DeadFour(row)[0] + DeadFour(col)[0]
            blackFreqStats[3] += LiveThree(row)[0] + LiveThree(col)[0]
            blackFreqStats[4] += DeadThree(row)[0] + DeadThree(col)[0]
            blackFreqStats[5] += LiveTwo(row)[0] + LiveTwo(col)[0]
            blackFreqStats[6] += DeadTwo(row)[0] + DeadTwo(col)[0]

            whiteFreqStats[0] += FiveInRow(row)[1] + FiveInRow(col)[1]
            whiteFreqStats[1] += LiveFour(row)[1] + LiveFour(col)[1]
            whiteFreqStats[2] += DeadFour(row)[1] + DeadFour(col)[1]
            whiteFreqStats[3] += LiveThree(row)[1] + LiveThree(col)[1]
            whiteFreqStats[4] += DeadThree(row)[1] + DeadThree(col)[1]
            whiteFreqStats[5] += LiveTwo(row)[1] + LiveTwo(col)[1]
            whiteFreqStats[6] += DeadTwo(row)[1] + DeadTwo(col)[1]

        for d in range(-len(self.map) + 1, len(self.map)): # get total frequency statistics for diagonal
            diagonal = np.diagonal(self.map, offset=d)
            blackFreqStats[0] += FiveInRow(diagonal)[0]
            blackFreqStats[1] += LiveFour(diagonal)[0]
            blackFreqStats[2] += DeadFour(diagonal)[0]
            blackFreqStats[3] += LiveThree(diagonal)[0]
            blackFreqStats[4] += DeadThree(diagonal)[0]
            blackFreqStats[5] += LiveTwo(diagonal)[0]
            blackFreqStats[6] += DeadTwo(diagonal)[0]

            whiteFreqStats[0] += FiveInRow(diagonal)[1]
            whiteFreqStats[1] += LiveFour(diagonal)[1]
            whiteFreqStats[2] += DeadFour(diagonal)[1]
            whiteFreqStats[3] += LiveThree(diagonal)[1]
            whiteFreqStats[4] += DeadThree(diagonal)[1]
            whiteFreqStats[5] += LiveTwo(diagonal)[1]
            whiteFreqStats[6] += DeadTwo(diagonal)[1]

        for d in range(-len(self.map) + 1, len(self.map)): # get total frequency statistics for anti diagonal
            diagonal = np.diagonal(np.fliplr(self.map), offset=d)
            blackFreqStats[0] += FiveInRow(diagonal)[0]
            blackFreqStats[1] += LiveFour(diagonal)[0]
            blackFreqStats[2] += DeadFour(diagonal)[0]
            blackFreqStats[3] += LiveThree(diagonal)[0]
            blackFreqStats[4] += DeadThree(diagonal)[0]
            blackFreqStats[5] += LiveTwo(diagonal)[0]
            blackFreqStats[6] += DeadTwo(diagonal)[0]

            whiteFreqStats[0] += FiveInRow(diagonal)[1]
            whiteFreqStats[1] += LiveFour(diagonal)[1]
            whiteFreqStats[2] += DeadFour(diagonal)[1]
            whiteFreqStats[3] += LiveThree(diagonal)[1]
            whiteFreqStats[4] += DeadThree(diagonal)[1]
            whiteFreqStats[5] += LiveTwo(diagonal)[1]
            whiteFreqStats[6] += DeadTwo(diagonal)[1]
            
        if blackFreqStats[0] != 0: # five in row 
            scoreTotal += 100000
        if blackFreqStats[1] == 1: # live four
            scoreTotal += 15000
        if blackFreqStats[3] >= 2 or blackFreqStats[2] == 2 or blackFreqStats[2] == blackFreqStats[3] == 1:
            scoreTotal += 10000
        if blackFreqStats[3] != 0:
            scoreTotal += 4000
        if blackFreqStats[2] != 0:
            scoreTotal += 1000
        if blackFreqStats[4] != 0:
            scoreTotal += 500
        if blackFreqStats[5] != 0:
            scoreTotal += 500
        if blackFreqStats[6] != 0:
            scoreTotal += 100

        if whiteFreqStats[0] != 0: # five in row 
            scoreTotal -= 100000
        if whiteFreqStats[1] == 1: # live four
            scoreTotal -= 15000
        if whiteFreqStats[3] >= 2 or whiteFreqStats[2] == 2 or whiteFreqStats[2] == whiteFreqStats[3] == 1:
            scoreTotal -= 10000
        if whiteFreqStats[3] != 0:
            scoreTotal -= 4000
        if whiteFreqStats[2] != 0:
            scoreTotal -= 1000
        if whiteFreqStats[4] != 0:
            scoreTotal -= 500
        if whiteFreqStats[5] != 0:
            scoreTotal -= 500
        if whiteFreqStats[6] != 0:
            scoreTotal -= 100

        return scoreTotal


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