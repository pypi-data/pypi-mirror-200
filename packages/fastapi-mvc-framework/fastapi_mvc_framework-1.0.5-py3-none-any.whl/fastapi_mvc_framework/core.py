from typing import Any,Dict
import uvicorn
from fastapi import FastAPI,UploadFile,File,Header, Depends,HTTPException,Request,Response,WebSocket,WebSocketDisconnect
from fastapi.security import OAuth2PasswordBearer
from .controller import create_controller,controller as api,   register_controllers_to_app
from .session import Session, FileStorage,MemoryStorage,SessionManager,_SESSION_STORAGES
from pydantic import BaseModel 
from .controller_utils import  TEMPLATE_PATH_KEY, VER_KEY,get_docs
import time,os,inspect
from fastapi import FastAPI, Cookie,Request
 
import datetime  
from starlette.responses import FileResponse


from .config import config,ROOT_PATH,_log
from fastapi.staticfiles import StaticFiles





async def on_appstart(*args,**kwargs):
   
    pass
__app = FastAPI(on_startup=[on_appstart]) 
__app_views_dirs = {} 
__all_controller__ = []

application = __app

def api_router(path:str="", version:str=""):  
    '''
    path :special path format ,
    '''
    caller_frame = inspect.currentframe().f_back
    caller_file = caller_frame.f_code.co_filename
    relative_path = caller_file.replace(ROOT_PATH,"")
    if relative_path.count(os.sep)>2:
        app_dir = os.path.dirname(os.path.dirname(relative_path)).replace(os.sep,"")
    else:
        app_dir = "app"
    app_dir = os.path.join(ROOT_PATH,app_dir)

    def format_path(p,v):
        if p and  '{controller}' not in p :
            p += '/{controller}' 
            p += '/{version}' if v else ''
        if v and not path:
            p = "/{controller}/{version}"
        return p
    path = format_path(path,version) 
    _controllerBase = create_controller(path,version)  
        
    __all_controller__.append(_controllerBase)
    
    def _wapper(targetController):  
        # 定义一个傀儡类，继承自目标类  
        class puppetController( targetController ,_controllerBase ): 
            
            def __init__(self,**kwags) -> None: 
                super().__init__()
            
                 
        setattr(puppetController,"__name__",targetController.__name__)  
        setattr(puppetController,"__controller_name__",targetController.__name__.lower().replace("controller",""))  
        
        setattr(puppetController,"__version__",version)  
        setattr(puppetController,"__location__",relative_path)  
        setattr(puppetController,"__appdir__",app_dir)  

        setattr(puppetController,"__controler_url__",targetController.__name__.lower().replace("controller",""))  
        #for generate url_for function
        _view_url_path:str = "/" + os.path.basename(app_dir) + '_views'  
         
        setattr(puppetController,"__view_url__",_view_url_path) 

        #add app dir sub views to StaticFiles
        if not app_dir in __app_views_dirs:
            __app_views_dirs[app_dir] = os.path.join(app_dir,"views")
            #path match static files
            _static_path = _view_url_path              
            __app.mount(_static_path,  StaticFiles(directory=__app_views_dirs[app_dir]), name=os.path.basename(app_dir))
 
        return puppetController 
    return _wapper #: @puppetController 

from fastapi import FastAPI, HTTPException,exceptions
 
from fastapi.responses import HTMLResponse
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback
__is_debug=False
@__app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e:StarletteHTTPException):
    content = "<h1>404 Not Found(URL Exception)</h1>"
    content += '<h3>please check url</h3>'
    if __is_debug:
        content += '<p>' + str(e.detail) + '</p>'
    return HTMLResponse(content=content, status_code=404)
    _log.error(f"OMG! An HTTP error!: {repr(exc)}")
    return await http_exception_handler(request, exc)#by default handler

@__app.exception_handler(Exception)
async def validation_exception_handler(request, e:Exception):
    content = "<h1>500 Internal Server Error</h1>"
    if __is_debug: 
        exc_traceback = e.__traceback__ 
        # show traceback the last files and location
        tb_summary = traceback.extract_tb(exc_traceback)[-3:]
        content += '<p>'
        for filename, line, func, text in tb_summary: 
            content += (f"{filename}:{line} in {func}</br>") 
        content += '</p>'
        content += '<p>Error description:' + str(e.args)  + '</p>'
    return HTMLResponse(content=content, status_code=500)


@__app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    _log.error(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

 
public_dir =  os.path.abspath(config.get("public_dir" ) )
if not os.path.exists(public_dir):
    os.mkdir(public_dir)

__app.mount('/public',  StaticFiles(directory=public_dir), name='public')

# @__app.get("/favicon.ico")
# def _get_favicon():
#     return FileResponse("./public/favicon.ico")
@__app.middleware("http")
async def preprocess_request(request: Request, call_next):
    _log.debug(f"dispatch on preprocess_request")
    if __is_debug:
        start_time = time.time() 
    #pre call to controller method
    response:Response = await call_next(request)

    if __is_debug:
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)  
    return response 

def generate_mvc_app(isDebug):
    if not len(__all_controller__)>0:
        raise "must use @api_route to define a controller class"
    all_routers = []
    all_routers_map = {}
    for ctrl in __all_controller__:
        all_routers.append(register_controllers_to_app(__app, ctrl))
    for router in all_routers:
        for r in router.routes:
            funcname = str(r.endpoint).split('<function ')[1].split(" at ")[0] 
            doc_map =  get_docs(r.description) if hasattr(r,'description') else {}
            if hasattr(r,'methods'):
                methods = r.methods
            else:
                methods = r.name
            if isDebug: 
                _log.debug(f"*****{methods}   \033[1;43m {r.path} \033[0m ->({funcname})" )
            all_routers_map[funcname] = {'path':r.path,'methods':methods,'doc':doc_map}
    application.routers_map = all_routers_map  
    return application

def run(app,*args,**kwargs): 
    global __is_debug
    host =  "host" in kwargs  and kwargs["host"]  or '0.0.0.0' 
    port = "port" in kwargs  and kwargs["port"] or 8000  
    __is_debug = "debug" in kwargs and kwargs["debug"]   
     
    uvicorn.run(app, host=host, port=port)