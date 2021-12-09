import asyncio
import websockets
import tkinter as tk
from tkinter import messagebox
    
async def time(websocket):
    flag:bool
    flag=1
    while True:
        message="0,0,0,0,0,0,0"
        message=input("Please enter the array:")
        
        """     if(flag):
            message="0,90,0,0,0,0,100"
            flag=0
        else:
            message="0,0,0,0,0,0,0"
            flag=0 """
        #now="{\"sender\":\"1\",\"recipient\":\"2\",\"content\":\""+message+"\"}"
        #print(now)
        await websocket.send('0,'+message)
        await asyncio.sleep(6) 


if __name__ == '__main__':
    start_server=websockets.serve(time,"127.0.0.1",8282)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()









