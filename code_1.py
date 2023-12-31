#!/usr/bin/env python3
import pygame
from math import sqrt 
from random import choice
import time
WIDTH,HEIGHT = 1020,700
cells_len = 20 
MAX_FPS = 60
WHITE =(237,246,220)
BLACK = (10,117,145)
GREEN = (0,255,0)
RED = (255,0,0)
COLOR1=(76,206,132)
pygame.init()
window = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("pong game")
font = pygame.font.Font(None,30)
class cell:
    def __init__(self,x,y):
        '''defining a normal cell which is not a wall at the beginning'''
        self.x =x 
        self.y= y
        self.possible_next = ['r','l','u','d','ur','ul','dr','dl']
        self.is_wall = False
        self.is_start = False
        self.is_end = False
        self.is_visited = False
        self.is_path = False
        self.parent = None
    def draw(self,window):
        '''draw the paddle'''
        color = WHITE
        if self.is_wall == True:
            color = BLACK
        elif self.is_start == True:
            color = GREEN
        elif self.is_end == True:
            color = RED
        elif self.is_path == True:
            color = (200,200,0)
        elif self.is_visited == True:
            color = (180,150,60)
        pygame.draw.rect(window,color,(self.x*cells_len+2 ,self.y*cells_len+2 ,cells_len-4 ,cells_len -4))

tab = [[cell(i,j)for i in range(WIDTH//cells_len)] for j in range(HEIGHT//cells_len-2)]

def fill_window(grid,diagonals):
    '''draw the image in the window'''
    window.fill(COLOR1)
    for line in grid:
        for cell in line:
            cell.draw(window)

    pygame.draw.rect(window, (0, 0, 0), (cells_len, HEIGHT -2*cells_len + cells_len//4, cells_len*6, cells_len*1.5))
    pygame.draw.rect(window, (237,246,220), (cells_len+2, HEIGHT -2*cells_len + cells_len//4+2, cells_len*6-4, cells_len*1.5-4))
    text_surface = font.render('dijkstra', True, (0,0,0))
    window.blit(text_surface, (3*cells_len-10,HEIGHT -2*cells_len + cells_len//2+2))

    pygame.draw.rect(window, (0, 0, 0), (8*cells_len, HEIGHT -2*cells_len + cells_len//4, cells_len*6, cells_len*1.5))
    pygame.draw.rect(window, (237,246,220), (8*cells_len+2, HEIGHT -2*cells_len + cells_len//4+2, cells_len*6-4, cells_len*1.5-4))
    text_surface = font.render('a star', True, (0,0,0))
    window.blit(text_surface, (10*cells_len-4,HEIGHT -2*cells_len + cells_len//2+2))

    # draw a switch for diagonals
    switch_size = cells_len
    switch_x = WIDTH - 3*switch_size
    switch_y = HEIGHT -1.5*cells_len 
    pygame.draw.rect(window, WHITE, (switch_x, switch_y, 2*switch_size, switch_size))
    pygame.draw.rect(window, (0, 0, 0), (switch_x + 2, switch_y + 2, 2*switch_size - 4, switch_size - 4))
    
    # Draw the switch handle
    switch_color = (0, 255, 0) if diagonals else (255, 0, 0)
    handle_size = switch_size // 2
    handle_x = switch_x + 2 if diagonals else switch_x + switch_size + 2
    pygame.draw.rect(window, switch_color, (handle_x, switch_y + 2, 2*handle_size-4, switch_size - 4))
    text_surface = font.render('Are diagonal movements allowed?', True, (0,0,0))
    window.blit(text_surface, (30*cells_len-4,HEIGHT -2*cells_len + cells_len//2+2))


    pygame.display.update()

def reset(diagonals):
    for line in tab:
        for cell in line:
            cell.is_end = False
            cell.is_start =False
            cell.is_wall = False
            cell.is_path = False
            cell.is_visited = False
            cell.parent = None
            if diagonals:
                cell.possible_next = ['r','l','u','d','ur','ul','dr','dl']
            else:
                cell.possible_next = ['r','l','u','d']


def in_grid(a):
    '''checking if the given coordinates are in the grid or not'''
    i,j = a[0],a[1]
    if i >= 0 and i <= len(tab[0])-1 and j >= 0 and j <= len(tab)-1:
        return True
    return False

def change_to_path(i,j,diagonals):
    '''giving the coordinates of a wall cell switching it to a path'''
    cell = tab[j][i]
    if cell.is_wall == True and cell.is_start == False and cell.is_end == False:
        cell.is_wall = False
        if diagonals:
            to_change = [(i-1,j-1),(i,j-1),(i+1,j-1),(i-1,j),(i+1,j),(i-1,j+1),(i,j+1),(i+1,j+1)]
            s=0
            for elt in to_change:
                if in_grid(elt):
                    if s==0:
                        tab[elt[1]][elt[0]].possible_next.append('dr')
                    elif s==1:
                        tab[elt[1]][elt[0]].possible_next.append('d')
                    elif s==2:
                        tab[elt[1]][elt[0]].possible_next.append('dl')
                    elif s==3:
                        tab[elt[1]][elt[0]].possible_next.append('r')
                    elif s==4:
                        tab[elt[1]][elt[0]].possible_next.append('l')
                    elif s==5:
                        tab[elt[1]][elt[0]].possible_next.append('ur')
                    elif s==6:
                        tab[elt[1]][elt[0]].possible_next.append('u')
                    else:
                        tab[elt[1]][elt[0]].possible_next.append('ul')
                s+=1
        else:
            to_change = [(i,j-1),(i-1,j),(i+1,j),(i,j+1)]
            s=0
            for elt in to_change:
                if in_grid(elt):
                    if s==0:
                        tab[elt[1]][elt[0]].possible_next.append('d')
                    elif s==1:
                        tab[elt[1]][elt[0]].possible_next.append('r')
                    elif s==2:
                        tab[elt[1]][elt[0]].possible_next.append('l')
                    else:
                        tab[elt[1]][elt[0]].possible_next.append('u')
                s+=1

        pygame.draw.rect(window, (237,246,220), (i*cells_len+2, j*cells_len+2, cells_len-4, cells_len-4))
        pygame.display.update()

def change_to_wall(i,j,diagonals):
    '''switching the cell with the (i,j) coordinates to a wall'''
    cell_a = tab[j][i]
    if cell_a.is_wall == False and cell_a.is_start == False and cell_a.is_end == False:
        tab[j][i].is_wall = True
        if diagonals:
            to_change = [(i-1,j-1),(i,j-1),(i+1,j-1),(i-1,j),(i+1,j),(i-1,j+1),(i,j+1),(i+1,j+1)]
            s=0
            for elt in to_change:
                if in_grid(elt):
                    if s==0:
                        tab[elt[1]][elt[0]].possible_next.remove('dr')
                    elif s==1:
                        tab[elt[1]][elt[0]].possible_next.remove('d')
                    elif s==2:
                        tab[elt[1]][elt[0]].possible_next.remove('dl')
                    elif s==3:
                        tab[elt[1]][elt[0]].possible_next.remove('r')
                    elif s==4:
                        tab[elt[1]][elt[0]].possible_next.remove('l')
                    elif s==5:
                        tab[elt[1]][elt[0]].possible_next.remove('ur')
                    elif s==6:
                        tab[elt[1]][elt[0]].possible_next.remove('u')
                    else:
                        tab[elt[1]][elt[0]].possible_next.remove('ul')
                s+=1
        else:
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
        pygame.draw.rect(window, (10,117,145), (i*cells_len+2, j*cells_len+2, cells_len-4, cells_len-4))
        pygame.display.update()

def get_cord(cell):
    '''given a cell this funct returns the coordinates of this cell'''
    return (cell.x,cell.y)

def get_next(a,diagonals):
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
        elif elt == 'l':
            if in_grid((x-1,y)):
                l.append(tab[y][x-1])
        elif diagonals:
            if elt=='ur':
                if in_grid((x+1,y-1)):
                    l.append(tab[y-1][x+1])
            elif elt=='ul':
                if in_grid((x-1,y-1)):
                    l.append(tab[y-1][x-1])
            elif elt=='dr':
                if in_grid((x+1,y+1)):
                    l.append(tab[y+1][x+1])
            elif elt=='dl':
                if in_grid((x-1,y+1)):
                    l.append(tab[y+1][x-1])
        
    return l

def get_distance(coord1,coord2):
    '''calculate the ditance between two cells of coors 1 and 2 '''
    return sqrt((coord1[0]-coord2[0])**2+(coord1[1]-coord2[1])**2)
def get_nearest_neighbor(cell,dic,diagonals):
    '''given a cell this function returns the neighbor cell with the lowest distance from the start'''
    l = get_next(cell,diagonals)
    a = l[0]
    b = dic[get_cord(l[0])]
    for elt in l[1:]:
        d = dic[get_cord(elt)]
        if  d <b :
            a = elt
            b = d
    return a

def dijkstra_animation(start_end,diagonals):
    cells_dist = {(x, y): float('inf') for y in range(HEIGHT) for x in range(WIDTH)}
    cells_dist[get_cord(start_end[0])] = 0
    current = start_end[0]
    UnvisitedCellWithFiniteDistance = {get_cord(current):0}
    visited = []
    end_is_found = False
    while start_end[1] not in visited :
        next_cells = get_next(current,diagonals)
        for elt in next_cells:
            if elt == start_end[1]:
                end_is_found= True
            elif elt in visited:
                next_cells.remove(elt)
        current_coord = get_cord(current)
        current_distance = cells_dist[current_coord]
        for elt in next_cells:
            d = get_distance(current_coord,get_cord(elt))
            if current_distance + d < cells_dist[get_cord(elt)]:
                coord = get_cord(elt)
                cells_dist[coord] = current_distance + d
                UnvisitedCellWithFiniteDistance[coord] = current_distance + d
                pygame.draw.rect(window, (180,150,60), ((coord[0])*cells_len+2, (coord[1])*cells_len+2, cells_len-4, cells_len-4))
        visited.append(current)
        if current == start_end[1]:
            end_is_found = True
        tab[current_coord[1]][current_coord[0]].is_visited = True
        current.is_visited = True
        UnvisitedCellWithFiniteDistance.pop(current_coord)
        if len(UnvisitedCellWithFiniteDistance) == 0:
            print('no path is found')
            break
        current_coord = min(UnvisitedCellWithFiniteDistance, key=lambda k: UnvisitedCellWithFiniteDistance[k])
        current = tab[current_coord[1]][current_coord[0]]
        pygame.display.update()
    if end_is_found:
        current = start_end[1]
        while current is not start_end[0]:
            '''draw the shortest path starting from the end to the start'''
            current = get_nearest_neighbor(current,cells_dist,diagonals)
            current_coord = get_cord(current)
            tab[current_coord[1]][current_coord[0]].is_path = True
            fill_window(tab,diagonals)

def heuristic_dist(coord0,coord1,diagonals):
    x0 = coord0[0]
    y0 =coord0[1]
    x1 = coord1[0]
    y1 =coord1[1]
    l = min(abs(x0-x1),abs(y0-y1))
    L = max(abs(x0-x1),abs(y0-y1))
    if diagonals:
        return sqrt(2*(l**2))+L-l
    else:
        return L+l

def g_cost(start_end,coord,diagonals):
    #return sqrt((start_end[0].x -coord[0])**2+ (start_end[0].y -coord[1])**2)
    return heuristic_dist(get_cord(start_end[0]),coord,diagonals)

def h_cost(start_end,coord,diagonals):
    #return sqrt((start_end[1].x -coord[0])**2+ (start_end[1].y -coord[1])**2)
    return heuristic_dist(get_cord(start_end[1]),coord,diagonals)

def f_cost(start_end,coord,diagonals):
    return h_cost(start_end,coord,diagonals)+g_cost(start_end,coord,diagonals)

def change_to_cost_for_heapq(start_end,cell):
    coord = get_cord(cell)
    a = h_cost(start_end,coord)
    return (a,(coord[0],coord[1],a))

def get_neighbor_with_small_h_cost(cell,d,diagonals):
    next_list = get_next(cell,diagonals)
    for elt in next_list:
        coord = get_cord(elt)
        if coord in d:
            b = coord
            a = d[coord]
            break
    for elt in next_list:
        coord = get_cord(elt)
        if coord in d:
            if d[coord] <a :
                b = coord
                a = d[coord]
    return b

def next_cell(potentiel_next):
    '''l={}
    minimum = min(potentiel_next, key=lambda k: potentiel_next[k][1])
    for elt in potentiel_next:
        if potentiel_next[elt]== minimum:
            l[elt]=potentiel_next[elt]
    return min(l, key=lambda k: l[k][0])'''
    return  min(potentiel_next, key=lambda k: (potentiel_next[k][1], potentiel_next[k][0]))

def a_star_animation(start_end,diagonals):
    '''given a start point and an end point , this function does the simulation of a start algorithme for shortest path between them'''
    visited = {}
    potentiel_next = {} 
    potentiel_next[start_end[0]] = (f_cost(start_end,get_cord(start_end[0]),diagonals),h_cost(start_end,get_cord(start_end[0]),diagonals))
    no_path = False
    while start_end[1] not in visited:
        if len(potentiel_next)==0:
            print('no possible path')
            no_path=True
            break
        #current = min(potentiel_next, key=potentiel_next.get)
        current = next_cell(potentiel_next)
        del potentiel_next[current]
        visited[current] = f_cost(start_end,get_cord(current),diagonals)
        neighbors = get_next(current,diagonals)
        for cell in neighbors:
            if cell not in visited:
                if cell not in potentiel_next:
                    potentiel_next[cell]=(f_cost(start_end,get_cord(cell),diagonals),h_cost(start_end,get_cord(cell),diagonals))
                    pygame.draw.rect(window, (180,150,60), (cell.x*cells_len+2,cell.y*cells_len+2, cells_len-4, cells_len-4))
                    pygame.display.update()
                    cell.is_visited = True
                    cell.parent = current 
    if not no_path:
        current = start_end[1].parent
        while current is not None:
            current.is_path = True
            pygame.draw.rect(window, (200,200,0), (current.x*cells_len+2,current.y*cells_len+2, cells_len-4, cells_len-4))
            pygame.display.update()
            current = current.parent
def possible_next_maze(a):
    '''given a cell we check if we can still find another sell to go to when creating the maze'''
    i,j = a[0],a[1]
    l0 = [(i,j-2),(i-2,j),(i+2,j),(i,j+2)]
    l1=[]
    for elt in l0:
        if in_grid(elt):
            if tab[elt[1]][elt[0]].is_wall == False:
                l1.append(elt)
    return l1

def get_unvisited_neighbors(a,visited):
    '''given a cell we return its unvisited neighbors'''
    i,j = a[0],a[1]
    l0 = [(i,j-2),(i-2,j),(i+2,j),(i,j+2)]
    l1=[]
    for elt in l0:
        if in_grid(elt):
            if elt not in visited :
                l1.append(elt)
    return l1

def maze_generator(diagonals):
    n,m = WIDTH//cells_len,HEIGHT//cells_len
    for i in range(0,n,2):
        for j in range(0,m-2):
            change_to_wall(i,j,diagonals)
    for j in range(0,m-2,2):
        for i in range(0,n):
            change_to_wall(i,j,diagonals)
    visited = {}
    start = (1,1)
    stack = [start]
    visited[start]= True
    while stack :
        current =stack.pop()
        unv_neighbors=get_unvisited_neighbors(current,visited)
        if unv_neighbors:
            neighbor = choice(unv_neighbors)
            m,n = abs(current[0]+neighbor[0])//2,abs(current[1]+neighbor[1])//2
            change_to_path(m,n,diagonals)
            visited[neighbor]=True
            stack.append(current)
            stack.append(neighbor)
        else:
            while stack:
                '''keep looking for a cell where we can continue the maze'''
                current = stack.pop()
                unv_neighbors=get_unvisited_neighbors(current,visited)
                if unv_neighbors:
                    stack.append(current)
                    break
        pygame.display.update()

def diagonalize(diagonals):
    if not diagonals:
        for line in tab:
            for cell in line:
                if 'ul' in cell.possible_next:
                    cell.possible_next.remove('ul')
                if 'ur' in cell.possible_next:
                    cell.possible_next.remove('ur')
                if 'dl' in cell.possible_next:
                    cell.possible_next.remove('dl')
                if 'dr' in cell.possible_next:
                    cell.possible_next.remove('dr')
    else:
        for line in tab:
            for cell in line:
                if 'ul' not in cell.possible_next:
                    cell.possible_next.append('ul')
                if 'ur' not in cell.possible_next:
                    cell.possible_next.append('ur')
                if 'dl' not in cell.possible_next:
                    cell.possible_next.append('dl')
                if 'dr' not in cell.possible_next:
                    cell.possible_next.append('dr')


def main():
    start_end = []
    '''main fonc that displays the program window'''
    running= True
    diagonals = False
    while running:
        fill_window(tab,diagonals)
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            '''left click'''
            x, y = pygame.mouse.get_pos() 
            i,j = x//cells_len , y//cells_len
            specific_key = pygame.key.get_pressed()[pygame.K_w]
            if specific_key:
                change_to_path(i,j,diagonals)
                while pygame.key.get_pressed()[pygame.K_w] and pygame.mouse.get_pressed(num_buttons=3)[0]:
                    x, y = pygame.mouse.get_pos()
                    i,j = x//cells_len , y//cells_len
                    event = pygame.event.poll()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        break
                    if j<len(tab):
                        if in_grid((i,j)):
                            change_to_path(i,j,diagonals)
            elif j<len(tab):
                change_to_wall(i,j,diagonals)
                while pygame.mouse.get_pressed(num_buttons=3)[0]:
                    x, y = pygame.mouse.get_pos()
                    i,j = x//cells_len , y//cells_len
                    event = pygame.event.poll()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        break
                    if j<len(tab):
                        if in_grid((i,j)):
                            change_to_wall(i,j,diagonals)
            elif len(start_end) ==2 and cells_len+2<=x<=cells_len+2 + 6* cells_len and HEIGHT -2*cells_len + cells_len//4+2 <=y <=HEIGHT -2*cells_len + cells_len//4+2 + cells_len*1.5:
                while pygame.mouse.get_pressed(num_buttons=3)[0]:
                    event = pygame.event.poll()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        break
                x, y = pygame.mouse.get_pos()
                i,j = x//cells_len , y//cells_len
                (cells_len, HEIGHT -2*cells_len + cells_len//4, cells_len*6, cells_len*1.5)
                if cells_len+2<=x<=cells_len+2 + 6* cells_len and HEIGHT -2*cells_len + cells_len//4+2 <=y <=HEIGHT -2*cells_len + cells_len//4+2 + cells_len*1.5:
                    dijkstra_animation(start_end,diagonals)
            elif len(start_end) ==2 and 8*cells_len+2<=x<=8*cells_len+2+cells_len*6-4 and HEIGHT -2*cells_len + cells_len//4+2<=y <=HEIGHT -2*cells_len + cells_len//4+2 + cells_len*1.5:
                while pygame.mouse.get_pressed(num_buttons=3)[0]:
                    event = pygame.event.poll()
                    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                        break
                x, y = pygame.mouse.get_pos()
                i,j = x//cells_len , y//cells_len
                (8*cells_len+2, HEIGHT -2*cells_len + cells_len//4+2, cells_len*6-4, cells_len*1.5-4)
                if 8*cells_len+2<=x<=8*cells_len+2+cells_len*6-4 and HEIGHT -2*cells_len + cells_len//4+2<=y <=HEIGHT -2*cells_len + cells_len//4+2 + cells_len*1.5:
                    a_star_animation(start_end,diagonals)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            '''right click'''
            x, y = pygame.mouse.get_pos()
            i,j = x//cells_len , y//cells_len
            if j<len(tab):
                if len(start_end)<2:
                    if tab[j][i].is_wall == False and tab[j][i].is_start == False and tab[j][i].is_end == False:
                        if len(start_end)==0:
                            tab[j][i].is_start = True
                        if len(start_end)==1:
                            tab[j][i].is_end = True
                        start_end.append(tab[j][i])
        elif event.type == pygame.KEYDOWN:
            if event.unicode.lower() == 'm':
                maze_generator(diagonals)
            if event.unicode.lower() == 'r':
                reset(diagonals)
                start_end=[]
            if event.unicode.lower() == 'd':
                allowed = True
                for line in tab:
                    if not allowed:
                        break
                    for cell in line:
                        if cell.is_wall :
                            allowed = False
                            text_surface = font.render('you have to reset before switching diagonals mode', True, (0,0,0))
                            window.blit(text_surface, (300,HEIGHT//2-50))
                            pygame.display.update()
                            time.sleep(3)
                            break
                if allowed:
                    diagonals = not diagonals
                    diagonalize(diagonals)
    pygame.quit()

if __name__ == '__main__':
    main()