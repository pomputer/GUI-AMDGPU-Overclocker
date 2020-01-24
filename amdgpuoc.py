#!/usr/bin/python3

#Copyright 2020 Patrick Babic

#This program is free software; you can redistribute it and/or modify
#it under the terms of the GNU  General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#MA 02110-1301, USA.

from tkinter import *
import os

memocfile='/sys/class/drm/card0/device/pp_mclk_od'
clkocfile='/sys/class/drm/card0/device/pp_sclk_od'
def checkInt(memocval, clkocval):
    try:
        int(memocval)
        int(clkocval)
        return True
    except ValueError:
        return False

def setResult(resultStr):
    resultStr='Output:\n' + resultStr
    result.config(text=resultStr)

def checkOrig(orig, current):
    if int(orig) > current:
        return False
    else:
        return True
def readFile(input, file):
    with open(file, 'r') as f:
        if checkOrig(f.read(), input):
            return True
        else:
            return False

def writeFile(input, file):
    with open(file, 'w') as f:
        f.write(str(input))

def getValues():
    if os.geteuid() == 0:
        memocval = memoc.get()
        clkocval = clkoc.get()
        if checkInt(memocval, clkocval):
            memocval = int(memocval)
            clkocval = int(clkocval)
            if readFile(memocval, memocfile) and readFile(clkocval, clkocfile):
                writeFile(memocval, memocfile)
                writeFile(clkocval, clkocfile)
                setResult('Success!')
            else:
                setResult('ERROR: Input lower than original. Restart required to restore stock clock speed.')
        else:
            setResult('ERROR: Input not a number')
    else:
        setResult('Permission Denied: This needs to be run as root.')

window = Tk()
window.title('AMDGPU overclock utility')
label = Label(window, text='AMDGPU overclock utility\nPlease input overclock percentages', font=('', 20))
label.pack()

labelclk = Label(window, text='Clock speed (%):', font=('', 10))
labelclk.pack()
clkoc = StringVar()
clkoco = Entry(window, textvariable=clkoc)
clkoco.pack()
clkoc.set('0')

labelmem = Label(window, text='Memory clock speed (%):', font=('', 10))
labelmem.pack()
memoc = StringVar()
memoco = Entry(window, textvariable=memoc)
memoco.pack()
memoc.set('0')

result = Label(window, text='Output:\n', font=('', 15))
result.pack()

submit = Button(window, text='Submit', bg='green', font=('', 20), command=getValues)
submit.pack()

window.mainloop()

