import tkinter as tk

import random
import string
from PIL import Image, ImageTk
from playsound3 import playsound
import colorsys


# генерация
s = str(input('Введите 6 цифр: '))

def clk():
    k = []
    b = [i for i in 'QWERTYUIOPASDFGHJKLZXCVBNM']

    l1 = random.sample(s[3:6], 3)
    l2 = random.sample(s[0:3], 3)


    for i in range(2):
        l1.append(random.choice(b))

    for i in range(2):
        l2.append(random.choice(b))

    l1 = ''.join(l1)
    l2 = ''.join(l2)
    l3 = str(int(str(l1[0:3])) + int(str(l2[0:3])))

    if len(l3)<4:
        l3 = '0' + l3

    k = [l1,l2,l3]

    key = '-'.join(k)

    lb2.config(text=key)

def gradient(lb, sthue=0.52):
    hue = sthue
    def anim():
        nonlocal hue
        r, g, b = colorsys.hls_to_rgb(hue, 0.8, 1)
        color = '#{:02x}{:02x}{:02x}'.format(int(r*255), int(g*255), int(b*255))
        lb.config(fg=color)
        hue += 0.002
        if hue > 0.85:
            hue = 0.52
        win.after(30,anim)
    anim()

#вывод
win = tk.Tk()
win.title('Генератор ключей для клеш рояль')
win.geometry('850x400')
music = playsound('music.mp3', block = False)

bg = Image.open('background.jpg')
bg = bg.resize((850, 400))
bg = ImageTk.PhotoImage(bg)
bgl = tk.Label(win, image=bg)
bgl.place(x=0, y=0, relwidth=1, relheight=1)

lb1 = tk.Label(win, text='Ключ активации 99999 гемов', font = ('Courier', 40), bg='#1b2030', fg='white')
lb1.place(x=5, y=25)
lb2 = tk.Label(win, text='XXXXX-XXXXX-XXXX', font = ('Courier', 50, 'bold'), bg='#15152a', fg='white')
lb2.place(x=90, y=180)
 
bt = tk.Button(win, text='Генерация', width=25, font = ('Courier', 25, 'bold'), background='#25254a', foreground= 'white',activebackground='#4545aa', activeforeground='white', command =clk)
bt.place(x=150, y=300)

gradient(lb1,0.52)
gradient(lb2,0.65)

win.mainloop()