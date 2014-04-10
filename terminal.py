#!/usr/bin/python

import time
from serial import Serial
import sys
from math import log
import Tkinter
connected=0
serialport=0


        


def bytes_needed(n):
    if n == 0:
        return 1
    return int(log(n, 256)) + 1
def ToHexList(num):
    lenght=bytes_needed(num)
    if lenght==0:
        return 0
    liste=[]
    for i in range(lenght):
        bitwise=0xff<<i*8
        liste.append(chr((num & bitwise)>>8*i))
    liste.reverse()
    return liste
def ToHexList2(num):
    lenght=bytes_needed(num)
    if lenght==0:
        return 0
    liste=[]
    for i in range(lenght):
        bitwise=0xff<<i*8
        liste.append(hex((num & bitwise)>>8*i))
    liste.reverse()
    return liste

def ToInt(liste):
	tal=0
	for i in range(len(liste)):
		tal+=liste[i]<<((len(liste)-(i+1))*8)
	return tal
def SerialConnect():
    global serialport
    serialport = Serial(port=PortPath.get(), baudrate=9600)
    global connected
    connected=1
    
def SendInput():
    if connected:
        command=InputString.get()
        command=int(command,16)
        command=ToHexList(command)
        serialport.write(command)
    
def Recive():
    reading=[]
    if connected:
        global RecievedString
        while (serialport.inWaiting()>0):							        
            if (serialport.inWaiting > 0):			
                reading.append(ord(serialport.read(1)))
            time.sleep(0.001)
        if reading!=[]:
            hexstring=''
            for i in reading:
                hexstring+=hex(i)[2:]+' '
            RecievedField.insert(Tkinter.INSERT,RecievedString.get()+hexstring+'\n')
    top.after(1,Recive)





top=Tkinter.Tk() #Main Windows
RWidth=top.winfo_screenwidth()
RHeight=top.winfo_screenheight()
top.minsize(50, 50)
top.maxsize(RWidth, RHeight)
InputString=Tkinter.StringVar() #String for the input window
RecievedString=Tkinter.StringVar()
PortPath=Tkinter.StringVar()
SendButton=Tkinter.Button(top,command=SendInput,text="Send",anchor='w') #Button to send
PortField=Tkinter.Entry(top,textvariable=PortPath)
PortField.grid(row=90, column=0, sticky="nsew")
ConnectButton=Tkinter.Button(top,command=SerialConnect,text="Connect")
ConnectButton.grid(row=90, column=1, sticky="nsew")
InputLabel=Tkinter.Label(top,text="Input:")
InputLabel.grid(row=100, column=0, sticky="nsew")

InputField=Tkinter.Entry(top,textvariable=InputString) #Field for user input
InputField.grid(row=110, column=0, sticky="nsew") #Show input Field
SendButton.grid(row=110, column=1, sticky="nsew") #Draw the button
RecievedScrool=Tkinter.Scrollbar(top)
RecievedScrool.grid(row=1200,column=1000,sticky="nsew")
RecievedField=Tkinter.Text(top,bg='white',yscrollcommand=RecievedScrool.set)
RecievedField.grid(row=1200,columnspan=999,  sticky="nsew")

#RecievedField.pack()
top.columnconfigure(0, weight=1)
top.columnconfigure(1, weight=1)
top.rowconfigure(100, weight=0) # not needed, this is the default behavior
top.rowconfigure(11, weight=0)
top.rowconfigure(120, weight=1)
top.after(1,Recive)
top.mainloop() #Start main loop

