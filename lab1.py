## Лабораторная работа №1 Ромашов Сергей вар. 10
## Флаг - Швейцария, узор - j, функция - y = x / 3, диаграмма - количество чисел от -3 до 3 и всех остальных

import time
import os

os.system("") ## чтобы поддерживались цвета в консоли Windows

RESET = '\u001b[0m'
BLACK = '\u001b[40m'
WHITE = '\u001b[47m'
RED = '\u001b[41m'
BLUE = '\u001b[44m'
ERASE = '\x1B[2K'
BEGIN = '\x1B[1G'

def clear():
    if os.name == 'nt':
        os.system('cls')    ## Windows
    else:
        os.system('clear')  ##Linux / macOS

# -------- флаг --------
def flag():
    size=11
    half=2
    centr=size//2
    for ryad in range(size):
        line=''
        for stolb in range(size):
            dist_ryad=abs(ryad-centr)
            dist_stolb=abs(stolb-centr) ## расстояние от текущей клетки до центр. ряда и центр. столбца

            ryad_u_centra=dist_ryad<=half//2 ## клетка рядом с центр. рядом или нет
            stolb_u_centra=dist_stolb<=half//2 ## клетка рядом с центр. столбцом или нет

            ins_ryad=ryad>=2 and ryad<=size-3 ## ряд не на границе флага
            ins_stolb=stolb>=2 and stolb<=size-3 ## столбец не на границе флага

            vert=stolb_u_centra and ins_ryad ## вертикальная полоса: столбец у центра, ряд не на границе
            hor=ryad_u_centra and ins_stolb ## горизонтальная полоса: ряд у центра, столбец не на границе

            if hor or vert:
                line+=f'{WHITE}  ' 
            else:
                line+=f'{RED}  '   

        print(line+RESET)


## -------- узор j --------

uzor = [
    '..***..',
    '.*...*.',
    '*.....*',
    '*.....*',
    '*.....*',
    '.*...*.',
    '..***..'

]

def draw(uzor):
    for ryad in uzor:
        line=''
        for simb in ryad:
            if simb=='*':
                line+=f'{BLUE}  '
            else:
                line+=f'{WHITE}  '
        print(line+RESET)

def pattern():
    count=4
    pic=[]
    for koltso_ryad in uzor:
        pic.append((koltso_ryad + '.')*count) ## повторяем узор count раз, добавляя точку между ними
    draw(pic)

## -------- анимация узора j --------
def animate():
    kadry=4 
    step=3 ## на сколько клеток сдвигаем узор вправо за один кадр
    loops=3
    for loop in range(loops):
        for kadr in range(kadry):
            clear()
            left='.'*(kadr*step)
            right='.'*((kadry-kadr-1)*step)
            pic=[]
            for koltso_ryad in uzor:
                pic.append(left+koltso_ryad+right)
            draw(pic)
            time.sleep(0.3)

## -------диаграмма количества чисел от -3 до 3 и всех остальных -------
def diagr():
    width=40
    numbs=[]
    file=open('sequence.txt')
    for line in file:
        if line.strip()!='':
            numbs.append(float(line))
    inside=0 ## от -3 до 3
    outside=0 ## все остальные
    for numb in numbs:
        if numb>=-3 and numb<=3:
            inside+=1
        else:
            outside+=1
    total=inside+outside
    percentinside=inside/total*100
    percentoutside=outside/total*100

    leninside=round(percentinside/100*width)
    lenoutside=round(percentoutside/100*width)
    print(f'от -3 до 3 {RED}{' '*leninside}{RESET} {percentinside:.1f}% ({inside})')
    print(f'остальные  {BLUE}{' '*lenoutside}{RESET} {percentoutside:.1f}% ({outside})')

## ------- график функции y=x/3 -------
def func(x):
    return x / 3

def graph():
    width=28 ## значения x: от 0 до 27
    height=10 ## строк в графике
    
    znach=[]

    for x in range(width):
        znach.append(func(x)) ##вычисляем значения функции 

    shag_y= max(znach)/(height-1) ## на сколько единиц увеличивается значение функции при переходе на следующую строку 

    grid=[]
    for ryad in range(height):
        grid_ryad=[]
        for stolb in range(width):
            grid_ryad.append(' ')
        grid.append(grid_ryad) ##создали пустую сетку

    for x in range(width):
        ryad=height- 1 - round(znach[x]/shag_y) ## так как 0 строка сверху, то нужно вычесть из высоты графика чтобы перевернуть график
        grid[ryad][x]='*' ## ставим звездочку в сетку в нужной позиции

    for ryad in range(height):
        y_lab=shag_y*(height-1-ryad) ## вычисляем значение функции для текущей строки
        line =f'{y_lab:4.0f} |' ## подпись оси y
        for stolb in range(width):
            if grid[ryad][stolb]=='*':
                line+= f'{RED} {RESET}'
            else: 
                line+=' '
        print(line) ## выводим сетку с подписью оси y



    print('     +' + '-' * width) 
    x_lab = '     '
    for x in range(0,width,3):
        x_lab+=f'{x:<3}'
    print(x_lab) ## ось x с подписями через каждые 3 клеток

## ------- готово, запускаем все функции -------
print('Ромашов Сергей ЛР1 вариант 10')
print('Флаг Швейцарии:')
flag()
print('Узор j:')
pattern()
print()
input('Нажмите Enter, чтобы увидеть анимацию узора j...')
print('Анимация узора j:')
animate()
print('Диаграмма количества чисел от -3 до 3 и всех остальных:')
diagr()
print('График функции y=x/3:')
graph()
