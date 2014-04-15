#!/usr/bin/python3

import time
from serial import Serial
import sys
from math import log
import tkinter
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
        for i in range(int(RepeatString.get())):
            serialport.write(command)
            time.sleep(0.001)
    
def Recive():
    reading=[]
    if connected:
        global RecievedString
        while (serialport.inWaiting()>0):							        
            if (serialport.inWaiting() > 0):			
                reading.append(ord(serialport.read(1)))
            time.sleep(0.001)
        if reading!=[]:
            hexstring=''
            for i in reading:
                hexstring+=hex(i)[2:]+' '
            RecievedField.insert(tkinter.INSERT,RecievedString.get()+hexstring+'\n')
            RecievedField.see('end')
    top.after(1,Recive)





top=tkinter.Tk() #Main Windows
RWidth=top.winfo_screenwidth()
RHeight=top.winfo_screenheight()
top.minsize(50, 50)
top.maxsize(RWidth, RHeight)
InputString=tkinter.StringVar() #String for the input window
RecievedString=tkinter.StringVar()
RepeatString=tkinter.StringVar()
RepeatString.set('1')
PortPath=tkinter.StringVar()
SendButton=tkinter.Button(top,command=SendInput,text="Send",anchor='w') #Button to send
PortField=tkinter.Entry(top,textvariable=PortPath)
PortField.grid(row=90, column=0, sticky="nsew")
ConnectButton=tkinter.Button(top,command=SerialConnect,text="Connect")
ConnectButton.grid(row=90, column=1, columnspan=2, sticky="nsew")
InputLabel=tkinter.Label(top,text="Input:")
InputLabel.grid(row=100, column=0, sticky="nsew")
RepeatLabel=tkinter.Label(top,text="Repeats:")

InputField=tkinter.Entry(top,textvariable=InputString) #Field for user input
RepeatField=tkinter.Entry(top,textvariable=RepeatString) #Field for user input
RepeatLabel.grid(row=100,column=1)
RepeatField.grid(row=100,column=2)
InputField.grid(row=110, column=0, sticky="nsew") #Show input Field
SendButton.grid(row=110, column=1, columnspan=2, sticky="nsew") #Draw the button
RecievedScrool=tkinter.Scrollbar(top)
RecievedScrool.grid(row=1200,column=1000,sticky="nsew")
RecievedField=tkinter.Text(top,bg='white',yscrollcommand=RecievedScrool.set)
RecievedField.grid(row=1200,columnspan=999,  sticky="nsew")

#RecievedField.pack()
top.columnconfigure(0, weight=1)
top.columnconfigure(1, weight=1)
top.rowconfigure(100, weight=0) # not needed, this is the default behavior
top.rowconfigure(11, weight=0)
top.rowconfigure(120, weight=1)
top.after(1,Recive)
top.mainloop() #Start main loop

