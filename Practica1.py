import time 
import curses
import os
import random
from curses import textpad
from curses import KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT



#Las opciones de mi menu 
op = ['1. Play', '2. Scoreboard', '3. User Selection','4. Reports', '5. Bulk Loading ']

def opciones(stdscr, Seleccion):
    stdscr.clear()
    h, w = stdscr.getmaxyx() #Variables para las coordenadas y x 
    for idx, row in enumerate(op):
        x = w//2 - len(row)//2
        y = h//2 - len(op)//2 + idx
        if (idx == Seleccion):
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y,x,row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y,x,row)
    stdscr.refresh()

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    actual = 0
    opciones(stdscr, actual)
    while 1:
        key = stdscr.getch()
        stdscr.clear()
        if key == curses.KEY_UP and actual > 0:
            actual -= 1
        elif key == curses.KEY_DOWN and actual < len(op)-1:
            actual += 1
        elif key == curses.KEY_ENTER or key in [10,13]:
            if (actual ==0):
                juego(stdscr)
            elif (actual == 1):
                puntuacion(stdscr)
            elif (actual == 2):
                usuario(stdscr)
            elif (actual == 3):
                reporte(stdscr)
            elif (actual == 4):
                carga(stdscr)
            stdscr.refresh()
            stdscr.getch()
            if (actual == len(op)-1):
                break

        opciones(stdscr, actual)
        stdscr.refresh()   

###### Creando snake ######
class NodoDoble():
    def __init__(self,posY, posX):
        self.siguiente = None
        self.anterior = None
        self.posX = posX
        self.posY = posY

class snake():
    #Creo el enlace al inicio, al final y el tamaño 
    def __init__(self):
        self.inicio = None 
        self.final = None
        self.size = 0 

    def Comer(self, posY, posX):
        nuevo = NodoDoble(posY, posX)
        nuevo.siguiente = self.inicio
        self.inicio.anterior = nuevo
        self.inicio = nuevo
        self.size += 1

    def eliminar(self):
        final.anterior.siguiente = None
        final = final.anterior

    def recorrer(self, stdscr):
        temp = self.inicio
        while(temp != None):
            x = temp.posX
            y = temp.posY
            temp = temp.siguiente



####### Comida ###########
def CrearComida(snake, box):
    Comida = None
    while Comida is None:
        Comida = [random.randint(box[0][0]+1, box[1][0]-1), 
        random.randint(box[0][1]+1, box[1][1]-1)]
        if Comida in snake:
            Comida = None
    return Comida

####### Pantallas ########
sn = snake()
def juego(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    h, w = stdscr.getmaxyx()
    area = [[4,4], [h-4, w-4]]
    textpad.rectangle(stdscr, area[0][0], area[0][1], area[1][0], area[1][1])
    #Primeros nodos, que no van a ser eliminados 
    snake = [[h//2, w//2+1], [h//2, w//2], [h//2, w//2-1]]
    direction = curses.KEY_RIGHT

    # draw snake
    for y,x in snake:
        stdscr.addstr(y, x, '#')

    # create food
    food = CrearComida(snake, area)
    stdscr.addstr(food[0], food[1], '*')

    # print score
    score = 0
    score_text = "Score: {}".format(score)
    stdscr.addstr(1, w//2 - len(score_text)//2, score_text)

    while 1:
        # non-blocking input
        key = stdscr.getch()

        # set direction if user pressed any arrow key
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP]:
            direction = key

        # find next position of snake head
        head = snake[0]
        if direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]
        elif direction == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]

        # insert and print new head
        stdscr.addstr(new_head[0], new_head[1], '#')
        snake.insert(0, new_head)

        # if sanke head is on food
        if snake[0] == food:
            # update score
            score += 1
            score_text = "Score: {}".format(score)
            stdscr.addstr(1, w//2 - len(score_text)//2, score_text)

            # create new food
            food = CrearComida(snake, area)
            stdscr.addstr(food[0], food[1], '*')

            # increase speed of game
            stdscr.timeout(100 - (len(snake)//3)%90)
        else:
            # shift snake's tail
            stdscr.addstr(snake[-1][0], snake[-1][1], ' ')
            snake.pop()

        # conditions for game over
        if (snake[0][0] in [area[0][0], area[1][0]] or 
            snake[0][1] in [area[0][1], area[1][1]] or 
            snake[0] in snake[1:]):
            msg = "Game Over!"
            stdscr.addstr(h//2, w//2-len(msg)//2, msg)
            stdscr.nodelay(0)
            stdscr.getch()
            break




def puntuacion(stdscr):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    area = [[4,4], [h-4, w-4]]
    textpad.rectangle(stdscr, area[0][0], area[0][1], area[1][0], area[1][1])
    stdscr.addstr(1, w//2 - len("Puntuacion")//2, "Puntuacion")
    
class NodoUsuario():
    def __init__(self, Nombre):
        self.siguiente = None
        self.anterior = None 
        self.Nombre = Nombre 

#Lista doble circular para los usuarios 
class Usuarios():
    def __init__(self):
        self.inicio = None
        self.final = None
        self.size = 0
    
    def Vacia(self):
        return self.size == 0

    def NuevoUser(self, Nombre):
        nuevo = NodoUsuario(Nombre)
        if(self.Vacia()):
            self.inicio = nuevo
            self.final = nuevo
            self.inicio.anterior = self.final
            self.final.siguiente = self.inicio
        else:
            self.final.siguiente = nuevo
            nuevo.anterior = self.final
            self.final = nuevo
            self.final.siguiente = self.inicio
            self.inicio.anterior = self.final
        self.size = self.size + 1

    def RecorrerUs(self, stdscr, dir, auxPos):
        h, w = stdscr.getmaxyx()
        if(self.Vacia()):
            stdscr.addstr(15, w//2-len("NO hay usuarios, ingrese un nombre")//2, "NO hay usuarios, ingrese un nombre")
        else: 
            stdscr.addstr(15, 10, "<-")
            stdscr.addstr(15, w//2-len(self.inicio.Nombre)//2, self.inicio.Nombre)
            stdscr.addstr(15, w-15, "->")
            if (dir == "der" and auxPos == self.size):
                temp = final.siguiente
                stdscr.addstr(15, 10, "<-")
                stdscr.addstr(15, w//2-len(temp.Nombre)//2, temp.Nombre)
                stdscr.addstr(15, w-15, "->")
            elif(dir == "der"):
                temp = self.inicio
                while (auxPos < self.size):
                    temp = temp.siguiente
                    stdscr.addstr(15, 10, "<-")
                    stdscr.addstr(15, w//2-len(temp.Nombre)//2, temp.Nombre)
                    stdscr.addstr(15, w-15, "->")
            elif (dir == "izq" and auxPos == 0):
                temp = self.final
                auxPos = self.size
                stdscr.addstr(15, 10, "<-")
                stdscr.addstr(15, w//2-len(temp.Nombre)//2, temp.Nombre)
                stdscr.addstr(15, w-15, "->")
            elif (dir == "izq"):
                temp = self.final
                auxPos = self.size
                while (auxPos > self.size):
                    temp = temp.anterior
                    auxPos = auxPos-1
                    stdscr.addstr(15, 10, "<-")
                    stdscr.addstr(15, w//2-len(temp.Nombre)//2, temp.Nombre)
                    stdscr.addstr(15, w-15, "->")
    
    def graficarUser(self):
        contador = 0
        if (self.Vacia()):
            print("No hay usuarios creados ")
        else:
            temp = self.inicio
            grafica = open("GraficarUsuarios.dot", "w")
            grafica.write("digraph G { \n")
            grafica.write("rankdir=LR  \n")
            grafica.write("node [shape= box, color=orange]; \n")
            #En el while guardo todos los nodos desde 0 
            contador = 0 
            while(contador < self.size):
                grafica.write("node"+ str(contador) + " [label = " + str(temp.Nombre)+"] \n")
                contador+= 1
                temp = temp.siguiente
            #Creando los enlaces hacia el final, menos el ultimo nodo
            for EDerecho in range(0,contador-1):
                grafica.write("node"+str(EDerecho)+" -> ")
            grafica.write("node"+str(contador-1) + " -> node0" ) #Imprimimos el ultimo nodo con enlace al primero
            #Creando los enlaces hacia el inicio, menos el primero
            grafica.write("\n")
            contador = contador-1
            while(contador != 0):
                grafica.write("node"+str(contador)+" -> ")
                contador = contador-1
            grafica.write("node0 -> node"+ str(self.size-1))

        grafica.write("\n")
        grafica.write("}")
        grafica.close()

        os.system("dot -Tjpg GraficarUsuarios.dot -o ListaDC_User.jpg")
        os.system("ListaDC_User.jpg")




def usuario(stdscr):
        auxPos = 0
        curses.curs_set(0)
        h, w = stdscr.getmaxyx()
        area = [[4,4], [h-4, w-4]]
        textpad.rectangle(stdscr, area[0][0], area[0][1], area[1][0], area[1][1])
        stdscr.addstr(1, w//2 - len("Usuarios")//2, "Usuarios")
        us = Usuarios()
        us.NuevoUser("Jeanifer")
        us.NuevoUser("Carlos")
        us.NuevoUser("Ale")
        while 1:
            key = stdscr.getch()
            stdscr.clear()
            if (key == curses.KEY_RIGHT):
                auxPos += 1
                us.RecorrerUs(stdscr, "der", auxPos)
            elif (key == curses.KEY_LEFT):
                auxPos = auxPos - 1
                us.RecorrerUs(stdscr, "izq", auxPos)

def reporte(stdscr):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    area = [[4,4], [h-4, w-4]]
    textpad.rectangle(stdscr, area[0][0], area[0][1], area[1][0], area[1][1])
    stdscr.addstr(1, w//2 - len("Reportes")//2, "Reportes")
    us = Usuarios()
    us.NuevoUser("Alejandrita")
    us.NuevoUser("Garcia")
    us.NuevoUser("Rodas")
    us.graficarUser()

def carga(stdscr):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    area = [[4,4], [h-4, w-4]]
    textpad.rectangle(stdscr, area[0][0], area[0][1], area[1][0], area[1][1])
    stdscr.addstr(1, w//2 - len("Carga masiva")//2, "Carga masiva")

curses.wrapper(main) 

