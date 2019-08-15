import time 
import curses
import os
import random
from curses import textpad
from curses import KEY_DOWN, KEY_UP, KEY_LEFT, KEY_RIGHT, KEY_F5, KEY_BACKSPACE, KEY_ALT_L

#Presionar 9 para regresar al menu principal 



#Las opciones de mi menu 
op = ['1. Play', '2. Scoreboard', '3. User Selection','4. Reports', '5. Bulk Loading ', '6. Exit']
reportes = ['a. Snake report', 'b. Score report', 'c. Scoreboard report', 'd. Users report', 'REGRESAR']
user = []

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

def elegirUser(stdscr, Seleccion):
    h, w = stdscr.getmaxyx() #Variables para las coordenadas y x 
    if user is None:
        stdscr.addstr("Ingrese nombre de usuario")
    else:
        for idx, row in enumerate(user):
            x = w//2 - len(row)//2
            y = h//2 - len(user)//2 + idx
            if (idx == Seleccion):
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y,x,row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y,x,row)
    stdscr.refresh()

def elegirReport(stdscr, Seleccion):
    h, w = stdscr.getmaxyx() #Variables para las coordenadas y x 
    if reportes is None:
        stdscr.addstr("Ingrese reporte")
    else:
        for idx, row in enumerate(reportes):
            x = w//2 - len(row)//2
            y = h//2 - len(reportes)//2 + idx
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
                DefinirUser(stdscr)
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
                main(stdscr)
        opciones(stdscr, actual)
        stdscr.refresh()   

def DefinirUser(stdscr):
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    actual0 = 0
    elegirUser(stdscr, actual0)
    while 1:
        key0 = stdscr.getch()
        stdscr.clear()
        if key0 == curses.KEY_UP and actual0 > 0:
            actual0 -= 1
        elif key0 == curses.KEY_DOWN and actual0 < len(user)-1:
            actual0 += 1
        elif key0 == curses.KEY_ENTER or key0 in [10,13]:
            juego(stdscr, user[actual0])
            stdscr.refresh()
            stdscr.getch()
            if (actual0 == len(user)-1):
                break
        elegirUser(stdscr, actual0)
        stdscr.refresh()

class PilaPunteo():
    def __init__(self):
        self.Punteos = []

    def Vacia(self):
        return self.Punteos == []

    def Agregar(self, posY, posX):
        self.Punteos.append((posY,posX))

    def Eliminar(self):
        return self.Punteos.pop()

    def Size(self):
        return len(self.Punteos)

    def GraficarPunteos(self):
        grafica = open("GraficarPunteos.dot", "w")
        grafica.write("digraph G { \n")
        grafica.write("node [shape=plaintext]  \n")
        grafica.write("some_node [ \n")
        grafica.write("label=< \n")
        grafica.write("<table border=\"0\" cellborder=\"1\" cellspacing=\"0\"> \n")
        grafica.write("<tr><td bgcolor=\"lightblue\"><font color=\"#0000ff\"> </font></td></tr>")
        for i in range(len(self.Punteos)):
            grafica.write("<tr><td bgcolor=\"lightblue\"><font color=\"#0000ff\"> ("+ str(self.Punteos[0]) + "," + str(self.Punteos[1])+")</font></td></tr> \n")
        grafica.write("</table>> \n")
        grafica.write("]; \n")
        grafica.write("}")
        grafica.close()
        os.system("dot -Tjpg GraficarPunteos.dot -o Pila.jpg")
        os.system("Pila.jpg")
            
        

        

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

    def Cabeza(self,stdscr, posY, posX):
        nuevo = NodoDoble(posY, posX)
        self.inicio = nuevo 
        self.final = nuevo 
        self.inicio.anterior = self.final
        self.final.siguiente = self.inicio
        #stdscr.addstr(posY, posX, '#')
    
    def Comer(self, stdscr, posY, posX): #Es añadir al final de lista
        nuevo = NodoDoble(posY, posX)
        nuevo.siguiente = self.inicio
        self.inicio.anterior = nuevo
        self.inicio = nuevo
        self.size += 1
        #stdscr.addstr(posY, posX, '#')

    def eliminar(self): #Elimino del final 
        final.anterior.siguiente = None
        final = final.anterior

    def Dibujar(self, stdscr): #imprimir la serpiente 
        temp = self.inicio
        indice = 0
        while(indice < self.size):
            x = temp.posX
            y = temp.posY
            #stdscr.addstr(y, x, '#')
            temp = temp.siguiente
            indice += 1

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
def juego(stdscr, Nombre):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)
    h, w = stdscr.getmaxyx()
    area = [[2,2], [h-2, w-2]]
    textpad.rectangle(stdscr, area[0][0], area[0][1], area[1][0], area[1][1])
    stdscr.addstr(1, 15, Nombre)
    #Primeros nodos, que no van a ser eliminados 
    sn.Cabeza(stdscr, h//2, w//2+1)
    sn.Comer(stdscr,h//2, w//2)
    sn.Comer(stdscr,h//2, w//2-1)
    snake = [[h//2, w//2+1], [h//2, w//2], [h//2, w//2-1]]
    direccion = curses.KEY_RIGHT
    # Dibujar la snake 
    #sn.Dibujar(stdscr)
    for y, x in snake:
        stdscr.addstr(y,x,'#')
    # Crear el + que aumenta el tamaño 
    Comida = CrearComida(snake, area)
    stdscr.addstr(Comida[0], Comida[1], '+')

    #Crear el * que disminuye el tamaño 
    #Comida = CrearComida(snake, area)
    #stdscr.addstr(Comida[0], Comida[1], '*')

    # Mostrar punteo 
    score = 0
    punteo = "Score: {}".format(score)
    stdscr.addstr(1, w//2 - len(punteo)//2, punteo)

    keystroke = -1
    while(keystroke==-1):
        keystroke = stdscr.getch()
        if (keystroke == 57):
            main(stdscr)
    
    while 1:
        key = stdscr.getch()
        if (key == 57):
            main(stdscr)
        # Guradamos la direccion que puede tomar, incluimos alt de la izquierda para retroceder
        if key in [curses.KEY_RIGHT, curses.KEY_LEFT, curses.KEY_DOWN, curses.KEY_UP, curses.KEY_ALT_L, curses.KEY_BACKSPACE]:
            direccion = key
        #Posicionarse en la lista doble enlazada. 
        head = snake[0]   
        if direccion == curses.KEY_RIGHT:
            new_head = [head[0], head[1]+1]
        elif direccion == curses.KEY_LEFT:
            new_head = [head[0], head[1]-1]
        elif direccion == curses.KEY_DOWN:
            new_head = [head[0]+1, head[1]]
        elif direccion == curses.KEY_UP:
            new_head = [head[0]-1, head[1]]

        # insert and print new head
        stdscr.addstr(new_head[0], new_head[1], '#')
        snake.insert(0, new_head)

        # if sanke head is on food
        if snake[0] == Comida:
            # update score
            score += 1
            score_text = "Score: {}".format(score)
            stdscr.addstr(1, w//2 - len(score_text)//2, score_text)

            # create new food
            Comida = CrearComida(snake, area)
            stdscr.addstr(Comida[0], Comida[1], '+')
            pilap = PilaPunteo()
            pilap.Agregar(Comida[0], Comida[1])

            #Cambiar de nivel 
            if (score == 2):
                stdscr.timeout(70)
                #stdscr.timeout(100 - (len(snake)//3)%90)
                stdscr.addstr(1, 100, "SEGUNDO NIVEL")
            elif (score == 4):
                stdscr.timeout(30)
                #stdscr.timeout(50 - (len(snake)//3)%120)
                stdscr.addstr(1, 100, "TERCER NIVEL")
                
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
            user.append(nuevo.Nombre)
        else:
            self.final.siguiente = nuevo
            nuevo.anterior = self.final
            self.final = nuevo
            self.final.siguiente = self.inicio
            self.inicio.anterior = self.final
            user.append(nuevo.Nombre)
        self.size = self.size + 1  
    
    def LlenarUs(self):
        temp = self.inicio
        indice = 0 
        while(indice < self.size):
            user.append(temp.Nombre)
            temp = temp.siguiente
            indice += 1
    
    def RecorrerUs(self, stdscr, dir, auxPos):
        curses.curs_set(0)
        h, w = stdscr.getmaxyx()
        area = [[4,4], [h-4, w-4]]
        textpad.rectangle(stdscr, area[0][0], area[0][1], area[1][0], area[1][1])
        stdscr.addstr(1, w//2 - len("Usuarios")//2, "Usuarios")
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

    def graficaUser(self):
        grafica = open("GraficarUsuarios.dot", "w")
        grafica.write("digraph G { \n")
        grafica.write("rankdir=LR  \n")
        grafica.write("node [shape= box, color=orange]; \n")
        #En el while guardo todos los nodos desde 0 
        i =1
        for i in range(len(user)):
            grafica.write("node"+str(i)+ " [label = "+ str(user[i])+"] \n")
        for i in range(len(user)-1):
            grafica.write("node"+str(i)+" -> ")
        grafica.write("node"+str(len(user)-1)+" \n")
        contador = len(user)-1
        while (contador > 0):
            grafica.write("node"+str(contador)+" -> ")
            contador = contador-1
        grafica.write("node0 \n")
        grafica.write("node0 -> node"+ str(len(user)-1)+"\n")
        grafica.write("node"+str(len(user)-1)+ " -> node0")
        grafica.write("\n")
        grafica.write("}")
        grafica.close()

        os.system("dot -Tjpg GraficarUsuarios.dot -o ListaDC_User.jpg")
        os.system("ListaDC_User.jpg")

def usuario(stdscr):
    us = Usuarios()
    auxPos = 0
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    area = [[4,4], [h-4, w-4]]
    textpad.rectangle(stdscr, area[0][0], area[0][1], area[1][0], area[1][1])
    stdscr.addstr(1, w//2 - len("Usuarios")//2, "Usuarios")
    actual = 0
    keystroke = -1
    while(keystroke==-1):
        keystroke = stdscr.getch()
        if (keystroke == 57):
            main(stdscr)
        elif (keystroke == 68):
            actual += 1
            us.RecorrerUs(stdscr, "der", actual)
        elif (keystroke == 65):
            us.RecorrerUs(stdscr, "izq", actual)

        
def reporte(stdscr):
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    area = [[4,4], [h-4, w-4]]
    textpad.rectangle(stdscr, area[0][0], area[0][1], area[1][0], area[1][1])
    stdscr.addstr(1, w//2 - len("Reportes")//2, "Reportes")
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    actual0 = 0
    elegirReport(stdscr, actual0)
    while 1:
        key0 = stdscr.getch()
        stdscr.clear()
        if key0 == curses.KEY_UP and actual0 > 0:
            actual0 -= 1
        elif key0 == curses.KEY_DOWN and actual0 < len(reportes)-1:
            actual0 += 1
        elif key0 == curses.KEY_ENTER or key0 in [10,13]:
            #if (actual0 ==0):
                #Graficar la doble enlazada snake 
            if (actual0 == 1):
                p = PilaPunteo()
                p.GraficarPunteos()
            #elif (actual0 == 2):
                #Graficar el usuario y su punteo 
            elif (actual0 == 3):
                u = Usuarios()
                u.graficaUser()
                stdscr.addstr(1,50,'Grafica de usuarios creada')
                main(stdscr)
            stdscr.refresh()
            stdscr.getch()
            if (actual0 == len(reportes)-1):
                main(stdscr)
        elegirReport(stdscr, actual0)
        stdscr.refresh()



def carga(stdscr):
    us = Usuarios()
    curses.curs_set(0)
    h, w = stdscr.getmaxyx()
    area = [[4,4], [h-4, w-4]]
    textpad.rectangle(stdscr, area[0][0], area[0][1], area[1][0], area[1][1])
    stdscr.addstr(1, w//2 - len("Carga masiva")//2, "Carga masiva")
    with open('Usuarios.csv', 'r') as archivo:
        linea = archivo.read().splitlines()
        linea.pop(0)
        for l in linea:
            linea = l.split(',')
            us.NuevoUser(linea[0])
            stdscr.addstr(15,30,linea[0])
    keystroke = -1
    while(keystroke==-1):
        keystroke = stdscr.getch()
        if (keystroke == 57):
            main(stdscr)

curses.wrapper(main) 

