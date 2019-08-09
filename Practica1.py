import time 
import curses
from curses import textpad

#Las opciones de mi menu 
op = ['1. Play', '2. Scoreboard', '3. User Selection','4. Reports', '5. Bulk Loading ']

def opciones(menu, Seleccion):
    menu.clear()
    h, w = menu.getmaxyx() #Variables para las coordenadas y x 
    for idx, row in enumerate(op):
        x = w//2 - len(row)//2
        y = h//2 - len(op)//2 + idx
        if (idx == Seleccion):
            menu.attron(curses.color_pair(1))
            menu.addstr(y,x,row)
            menu.attroff(curses.color_pair(1))
        else:
            menu.addstr(y,x,row)
    menu.refresh()


def main(menu):
    curses.curs_set(0) 
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    actual = 0
    opciones(menu, actual)
    while 1:
        key = menu.getch()
        menu.clear()
        if key == curses.KEY_UP and actual > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and actual < len(op)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10,13]:
            menu.addstr(0,0,"Presiono la tecla enter")
            menu.refresh()
            menu.getch()
            if (actual == len(op)-1):
                break

        opciones(menu, actual)
        menu.refresh()

curses.wrapper(main) 

