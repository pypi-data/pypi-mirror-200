# fastapi_framework
A mvc framework used FastApi
Simple and elegant use of FastApi in MVC mode

usage:


```

from fastapi_mvc_framework import api_router,api,Request,Response,BaseController,application,WebSocket,WebSocketDisconnect
import requests,openai,json

model_engine = "text-davinci-003"  # Or any other model
openai.api_key = 'sk-123456'
 

@api_router()
class TestController(BaseController):
    
    def __init__(self):
        self.log.info(f"__init__ on TestController")

    @api.get("/" )
    def home(self): 
        '''
        :title 首页
        '''
        c = self.session['home'] or 1
        c = c+1 
        # #setting cookies   
        # self.response.set_cookie('a',c) 
        self.cookies["a"] = c
        if c>10:
            del self.cookies["a"]
            c = 0
        self.session['home'] = c
        text = "Hello World! I'm in FastapiMvcFramework"
        routers_map = application.routers_map
        routers = application.routes
        return self.view()
    
    @api.http("/gpt-proxy",methods=['POST','GET'])
    async def proxy(self):

        prompt=""
        if 'prompt' in self.request.params :
            prompt = self.request.params['prompt']
        if not prompt:
            return {"msg":"empty"}
        return {"msg":prompt}
        response = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
         
        return (response).to_dict() 

    @api.post("/chatgptdemo")
    async def chatgpt_demo(self):
        
        message = self.request.params
        if message:
            response = openai.Completion.create(
                engine=model_engine,
                prompt=message['s'],
                max_tokens=1024,
                n=1,
                stop=None,
                temperature=0.5,
            )
         
        return response['choices'][0].text.strip()      

    @api.get("/chatgpt")
    def chatgpt(self):
        """
        :title 聊天
        """
        return self.view()


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/chat/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
manager = ConnectionManager()

@application.websocket("/ws/chat/{client_id}")
async def websocket_endpoint(websocket: WebSocket,client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

@api_router(path="/{controller}")
class WSController(BaseController): 
    @api.get("/" )
    def ws_home(self):
        """:title WebSocketDemo"""
        return self.view(content = html)


```
