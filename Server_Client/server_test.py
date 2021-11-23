import asyncio
import websockets
import tkinter as tk
from tkinter import messagebox

"""async def submit_mes(websocket):
    global e
    mes= str(e.get())
    print(mes)
    while True:
        # message=input("Please enter the array:")
        now="{\"sender\":\"1\",\"recipient\":\"2\",\"content\":\""+mes+"\"}"
        print(now)
        await websocket.send(now)
        await asyncio.sleep(1)"""
    
async def time(websocket):
    flag:bool
    flag=1
    while True:
        #message=input("Please enter the array:")
        if(flag):
            message="0,90,0,0,0,0,100"
            flag=0
        else:
            message="0,0,0,0,0,0,0"
            flag=1
        now="{\"sender\":\"1\",\"recipient\":\"2\",\"content\":\""+message+"\"}"
        print(now)
        await websocket.send(now)
        await asyncio.sleep() 


if __name__ == '__main__':
    start_server=websockets.serve(time,"127.0.0.1",8282)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

"""window=tk.Tk()
window.title('please enter the array')
window.geometry("300x300")
mes=tk.StringVar()
l1=tk.Label(window,width=200,height=6,text="Please enter the array input")
l1.pack()

e=tk.Entry(window,textvariable=mes)
e.pack()

b=tk.Button(window,text="submit",width=100,height=10,command=submit_mes)
b.pack()

if mes!=" ":
    start_server=websockets.serve(submit_mes,"127.0.0.1",8282)

    

window.mainloop()"""








