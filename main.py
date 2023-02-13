from nptdms import TdmsFile
import os
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

gui = Tk()
gui.geometry("400x400")
gui.title("Diadem reporter")

def getFolderPath():
    folder_selected = filedialog.askdirectory()
    folderPath.set(folder_selected)

def doStuff():
    minimum_tolerance = minimum.get()
    maksimum_tolerance = maksimum.get()
    quantity = 0
    position = 0
    counter = 0
    folder = folderPath.get()
    directory = os.fsencode(folder)
    e = Label(gui, text=f'File in progress: 0')
    e.grid(row=5, column=1)
    gui.update()
    with open(f'{result_name.get()}.csv', mode='w+', encoding='utf-8') as f:
        for file in os.listdir(directory):
            filename = os.fsdecode(file)
            if filename.endswith(".tdms"):
                tdms_file = TdmsFile.read(f'{folder}/{filename}')
                counter += 1
                e.configure(text=f'File in progress: {counter}')
                gui.update()
                for group in tdms_file.groups():
                    for channel in group.channels():
                        all_channels = channel[:]
                        if 'P22' in channel.name:
                            for prev, value in zip(all_channels, all_channels[1:]):
                                position += 1
                                if prev > 1 and value > 1:
                                    quantity += 1
                                else:
                                    if quantity > 1:
                                        if (quantity < minimum_tolerance or quantity > maksimum_tolerance) and position != 1:
                                            f.write(f'{filename}  {group.name} {channel.name} {position} {quantity}\n')
                                            quantity = 0
                                        else:
                                            quantity = 0
                        if quantity > 1:
                            if (quantity < minimum_tolerance or quantity > maksimum_tolerance) and position != 1:
                                f.write(f'{filename} \t {group.name} \t {channel.name} \t {position} \t {quantity}\n')
                        position = 0
                        quantity = 0

        gui.quit()

folderPath = StringVar()
minimum = IntVar()
maksimum = IntVar()
result_name = StringVar()

a = Label(gui ,text="Enter name")
a.grid(row=0,column = 0)
E = Entry(gui,textvariable=folderPath)
E.grid(row=0,column=1)
btnFind = ttk.Button(gui, text="Browse Folder",command=getFolderPath)
btnFind.grid(row=0,column=2)

b = Label(gui, text="Minimum")
b.grid(row=1, column=0)
E2 = Entry(gui, textvariable=minimum)
E2.grid(row=1,column=1)

c = Label(gui, text="Maksimum")
c.grid(row=2, column=0)
E3 = Entry(gui, textvariable=maksimum)
E3.grid(row=2,column=1)

d = ttk.Button(gui ,text="Run!", command= doStuff)
d.grid(row=4,column=0)

f = Label(gui ,text="Enter result file name")
f.grid(row=3,column = 0)
E4 = Entry(gui,textvariable=result_name)
E4.grid(row=3,column=1)

gui.mainloop()