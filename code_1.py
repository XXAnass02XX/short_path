#!/usr/bin/env python3
import pygame
import heapq
import time 
WIDTH,HEIGHT = 1800,900
cells_len = 30
MAX_FPS = 60
WHITE =(255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)
COLOR1=(155,0,155)
pygame.init()
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pong game")
font = pygame.font.Font(None,cells_len)
clock = pygame.time.Clock()
class cell:
    def __init__(self,x,y):
        '''defining a normal cell which is not a wall at the beginning'''
        self.x =x 
        self.y= y
        self.possible_next = ['r','l','u','d']
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.is_visited = False
        self.is_path = False
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
        elif self.is_path == True:
            color = (200,200,0)
        elif self.is_visited == True:
            color = (0,200,255)
        pygame.draw.rect(window,color,(self.x*cells_len+2 ,self.y*cells_len+2 ,cells_len-4 ,cells_len -4))
        #window.blit(text, (self.x*cells_len ,self.y*cells_len))

tab = [[cell(i,j)for i in range(WIDTH//cells_len)] for j in range(HEIGHT//cells_len-2)]

def fill_window(grid):
    '''draw the image in the window'''
    window.fill(COLOR1)
    for line in grid:
        for cell in line:
            cell.draw(window)

    pygame.draw.rect(window, (0, 0, 0), (cells_len, HEIGHT -2*cells_len + cells_len//2, cells_len*3, cells_len))
    pygame.draw.rect(window, (150, 50, 150), (cells_len+2, HEIGHT -2*cells_len + cells_len//2+2, cells_len*3-4, cells_len-4))
    text_surface = font.render('start', True, (0,0,0))
    window.blit(text_surface, (2*cells_len-4,HEIGHT -2*cells_len + cells_len//2+2))
    pygame.display.update()

def in_grid(a):
    '''checking if the given coordinates are in the grid or not'''
    i,j = a[0],a[1]
    if i >= 0 and i <= len(tab[0])-1 and j >= 0 and j <= len(tab)-1:
        return True
    return False

def change_to_wall(i,j):
    '''switching the cell with the (i,j) coordinates to a wall'''
    cell_a = tab[j][i]
    if cell_a.is_wall == False and cell_a.is_start == False and cell_a.is_end == False:
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
        pygame.draw.rect(window, (0, 0, 0), (i*cells_len+2, j*cells_len+2, cells_len-4, cells_len-4))
        pygame.display.update()

def get_cord(cell):
    '''given a cell this funct returns the coordinates of this cell'''
    return (cell.x,cell.y)

def get_next(a):
    '''given a cell this function returns a list of possible next cells'''
    l=[]
    for elt in a.possible_next:
        x , y = get_cord(a)
        if elt=='d':
            if in_grid((x,y+1)):
                l.append(tab[y+1][x])
        elif elt=='u':
            if in_grid((x,y-1)):
                l.append(tab[y-1][x])
        elif elt=='r':
            if in_grid((x+1,y)):
                l.append(tab[y][x+1])
        else:
            if in_grid((x-1,y)):
                l.append(tab[y][x-1])
    return l

def get_nearest_neighbor(cell,dic):
    '''given a cell this function returns the neighbor cell with the lowest distance from the start'''
    l = get_next(cell)
    a = l[0]
    b = dic[get_cord(l[0])]
    for elt in l[1:]:
        d = dic[get_cord(elt)]
        if  d <b :
            a = elt
            b = d
    return a

def dijkstra_animation(start_end):
    cells_dist = {(x, y): float('inf') for y in range(HEIGHT) for x in range(WIDTH)}
    cells_dist[get_cord(start_end[0])] = 0
    current = start_end[0]
    UnvisitedCellWithFiniteDistance = {get_cord(current):0}
    visited = []
    while start_end[1] not in visited :
        next_cells = get_next(current)
        for elt in next_cells:
            if elt in visited:
                next_cells.remove(elt)
        current_coord = get_cord(current)
        current_distance = cells_dist[current_coord]
        for elt in next_cells:
            if current_distance + 1 < cells_dist[get_cord(elt)]:
                coord = get_cord(elt)
                cells_dist[coord] = current_distance + 1
                UnvisitedCellWithFiniteDistance[coord] = current_distance + 1
                pygame.draw.rect(window, (100,200,255), ((coord[0])*cells_len+2, (coord[1])*cells_len+2, cells_len-4, cells_len-4))
        visited.append(current)
        tab[current_coord[1]][current_coord[0]].is_visited = True
        current.is_visited = True
        UnvisitedCellWithFiniteDistance.pop(current_coord)
        current_coord = min(UnvisitedCellWithFiniteDistance, key=lambda k: UnvisitedCellWithFiniteDistance[k])
        current = tab[current_coord[1]][current_coord[0]]
        pygame.display.update()
        #fill_window(tab)
    current = start_end[1]
    while current is not start_end[0]:
        '''draw the shortest path starting from the end to the start'''
        current = get_nearest_neighbor(current,cells_dist)
        current_coord = get_cord(current)
        tab[current_coord[1]][current_coord[0]].is_path = True
        fill_window(tab)
    return None

def main():
    start_end = []
    '''main fonc that displays the program window'''
    running= True
    while running:
        fill_window(tab)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            running= False
            break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            '''left click'''
            x, y = pygame.mouse.get_pos()
            i,j = x//cells_len , y//cells_len
            if j<len(tab):
                change_to_wall(i,j)
                while pygame.mouse.get_pressed(num_buttons=3)[0]:
                    x, y = pygame.mouse.get_pos()
                    i,j = x//cells_len , y//cells_len
                    event = pygame.event.poll()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        break
                    if j<len(tab):
                        change_to_wall(i,j)
            elif len(start_end) ==2 and cells_len+2<=x<=cells_len+2 + 3* cells_len and HEIGHT -2*cells_len + cells_len//2+2 <=y <=HEIGHT -2*cells_len + cells_len//2+2 + cells_len:
                while pygame.mouse.get_pressed(num_buttons=3)[0]:
                    event = pygame.event.poll()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        break
                x, y = pygame.mouse.get_pos()
                i,j = x//cells_len , y//cells_len
                if cells_len+2<=x<=cells_len+2 + 3* cells_len and HEIGHT -2*cells_len + cells_len//2+2 <=y <=HEIGHT -2*cells_len + cells_len//2+2 + cells_len:
                    dijkstra_animation(start_end)
                
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            '''right click'''
            x, y = pygame.mouse.get_pos()
            i,j = x//cells_len , y//cells_len
            if j<len(tab):
                if len(start_end)<2:
                    if tab[j][i].is_wall == False and tab[j][i].is_start == False and tab[j][i].is_end == False:
                        if len(start_end)==0:
                            tab[j][i].is_start = True
                            print("start, ")
                        if len(start_end)==1:
                            tab[j][i].is_end = True
                            print("end")
                        start_end.append(tab[j][i])
        elif event.type == pygame.KEYDOWN: 
            if event.unicode.lower() == 'r':
                for line in tab:
                    for cell in line:
                        cell.is_end = False
                        cell.is_start =False
                        cell.is_wall = False
                        cell.is_path = False
                        cell.is_visited = False
                        cell.possible_next = ['r','l','u','d']
                start_end = []
    pygame.quit()

if __name__ == '__main__':
    main()