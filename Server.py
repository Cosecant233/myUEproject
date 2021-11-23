import websockets
import asyncio
import threading
import json
import time

class MyServer:
    def __init__(self,host='127.0.0.1',port='8800'):
        self.__host=host
        self.__port=port
        self.__listcmd=[]
        self.__server=None
        self.__isExecute=False
        self.__message_value=None

    def __del__(self):
        self.stop_server()

    async def __consumer_handler(self,websocket,path):
        async for message in websocket:
            await self.__consumer(message)

    async def __producer_handler(self,websocket,path):
        while True:
            await asyncio.sleep(0.000001)
            message=await self.__producer()
            if(message):
                await websocket.send(message)

    async def __handler(self, websocket, path):
        consumer_task = asyncio.ensure_future(self.__consumer_handler(websocket, path))
        producer_task = asyncio.ensure_future(self.__producer_handler(websocket, path))
        done, pending = await asyncio.wait([consumer_task, producer_task], return_when=asyncio.FIRST_COMPLETED, )
        for task in pending:
            task.cancel()

    # 接收处理
    async def __consumer(self, message):
        print('recv message: {0}'.format(message))
        self.__isExecute = True
        # jsonContent=json.loads(message)
        # self.__isExecute=jsonContent['IsExecute']
        # self.__message_value=jsonContent['Value']

    # 发送处理
    async def __producer(self):
        if len(self.__listcmd) > 0:
            return self.__listcmd.pop(0)
        else:
            return None

    # 创建server
    def __connect(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        print('start connect')
        self.__isExecute = True
        if self.__server:
            print('server already exist')
            return
        self.__server = websockets.serve(self.__handler, self.__host, self.__port)
        asyncio.get_event_loop().run_until_complete(self.__server)
        asyncio.get_event_loop().run_forever()

    # 往要发送的命令列表中，添加命令
    def __add_cmd(self, topic, key, value=None):
        self.__message_value = None
        while self.__isExecute == False:  # 没有收到处理
            pass
        content = {'Topic': topic, 'Data': {'Key': key, 'Value': value}}
        jsonObj = json.dumps(content)
        self.__listcmd.append(jsonObj)
        print('add cmd: {0}'.format(content))
        self.__isExecute = False

    ##################################################
    # public
    ##################################################

    # 开启服务
    def start_server(self):
        print('start server at {0}:{1}'.format(self.__host, self.__port))
        t = threading.Thread(target=self.__connect)
        t.start()

    # 关闭服务
    def stop_server(self):
        print('stop server at {0}:{1}'.format(self.__host, self.__port))
        if self.__server is None:
            return
        self.__server.ws_server.close()
        self.__server = None

    # 发送时间
    def send_time(self):
       self.__add_cmd('15','5')
       #self.__add_cmd('Unreal', 'Time', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()))

def main():
    s=MyServer('127.0.0.1',8800)
    s.start_server()

    count=0
    while count < 5:
        s.send_time()
        count+=1

    s.stop_server()

if __name__ == '__main__':
    main()