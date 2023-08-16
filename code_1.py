#!/usr/bin/env python3
import pygame

WIDTH,HEIGHT = 1800,900
cells_len = 50
MAX_FPS = 60
WHITE =(255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
COLOR1=(155,0,155)
pygame.init()
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pong game")
font = pygame.font.Font(None,30)
start_end = []
class cell:
    def __init__(self,x,y):
        '''defining a normal cell which is not a wall at the beginning'''
        self.x =x 
        self.y= y
        self.possible_next = ['r','l','u','d']
        self.is_wall = False
        self.is_start = False
        self.is_end = False
    def draw(self,window):
        '''draw the paddle'''
        color = WHITE
        text = font.render(f'{self.x},{self.y}', True, (0, 255, 255))
        if self.is_wall == True:
            color = BLACK
        elif self.is_start == True:
            color = GREEN
        elif self.is_end == True:
            color = RED
        pygame.draw.rect(window,color,(self.x*cells_len+2 ,self.y*cells_len+2 ,cells_len-4 ,cells_len -4))
        #window.blit(text, (self.x*cells_len ,self.y*cells_len))

tab = [[cell(i,j)for i in range(WIDTH//cells_len)] for j in range(HEIGHT//cells_len-2)]

def fill_window(grid):
    '''draw the image in the window'''
    window.fill(COLOR1)
    for line in grid:
        for cell in line:
            cell.draw(window)
    pygame.display.update()

def in_grid(a):
    '''checking if the given coordinates are in the grid or not'''
    i,j = a[0],a[1]
    if i >= 0 and i <= len(tab[0])-1 and j >= 0 and j <= len(tab)-1:
        return True
    return False

def change_to_wall(i,j):
    '''switching the cell with the (i,j) coordinates to a wall'''
    if tab[j][i].is_wall == False and tab[j][i].is_start == False and tab[j][i].is_end == False:
        tab[j][i].is_wall = True
        to_change = [(i,j-1),(i-1,j),(i+1,j),(i,j+1)]
        s=0
        for elt in to_change:
            if in_grid(elt):
                if s==0:
                    tab[elt[1]][elt[0]].possible_next.remove('d')
                elif s==1:
                    tab[elt[1]][elt[0]].possible_next.remove('r')
                elif s==2:
                    tab[elt[1]][elt[0]].possible_next.remove('l')
                else:
                    tab[elt[1]][elt[0]].possible_next.remove('u')
            s+=1
def main():
    '''main fonc that displays the program window'''
    running= True
    while running:
        fill_window(tab)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running= False
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    '''left click'''
                    x, y = pygame.mouse.get_pos()
                    i,j = x//cells_len , y//cells_len
                    #print("Right-click detected at:", x//50, y//50)
                    #TODO 
                    '''verifier ce -21'''
                    if j<=WIDTH//cells_len-21:
                        change_to_wall(i,j)
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    '''right click'''
                    x, y = pygame.mouse.get_pos()
                    i,j = x//cells_len , y//cells_len
                    if j<=WIDTH//cells_len-21:
                        if len(start_end)<2:
                            if tab[j][i].is_wall == False and tab[j][i].is_start == False and tab[j][i].is_end == False:
                                if len(start_end)==0:
                                    tab[j][i].is_start = True
                                    print("start, ")
                                if len(start_end)==1:
                                    tab[j][i].is_end = True
                                    print("end")
                                start_end.append((i,j))
                                

    pygame.quit()

if __name__ == '__main__':
    main()