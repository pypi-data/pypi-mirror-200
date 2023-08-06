from .session import Session, FileStorage,MemoryStorage,SessionManager,_SESSION_STORAGES
from fastapi import FastAPI,UploadFile,File,Header, Depends,HTTPException,Request,Response
from fastapi.responses import RedirectResponse,HTMLResponse,PlainTextResponse
from .view import _View
from .config import config,ROOT_PATH,_log
import os
from hashlib import md5
from typing import Dict
from logging import Logger
import inspect

__session_config = config.get('session') 
_sessionManager = SessionManager(storage=_SESSION_STORAGES[__session_config['type']](__session_config['dir'],__session_config['secretkey']))



class BaseController:
    
    def __init__(self) -> None:
        
        
        _log.debug('__init__ on BaseController')
    @property
    def log(self)->Logger:
        return _log
    @property 
    def cookies(self)->Dict[str,str]: 
        return self._cookies 
    
    @property
    def request(self)->Request :
        return self._request
    # @request.setter
    # def request(self,value):
    #     self.__request = value
    @property
    def response(self)->Response :
        return self._response
    # @response.setter
    # def response(self,value):
    #     self.__response = value
    @property
    def session(self)->Session:
        return self._session  
    
    def redirect(self,url):
        return RedirectResponse(url)
    
     
    # @property
    def view(self,content:str="",view_path:str="", format:str="html", context: dict={},local2context:bool=True): 
        def url_for(url:str="",type:str="static",**kws):
            url_path :str = self.__view_url__ 
            url = url.strip()
            if type!='static' or kws: #url route
                if kws:
                    url_path = ""
                    pairs = []
                    if 'app' in kws and kws['app'].strip():
                        pairs.append(kws['app'].strip())
                    if 'controller' in kws  and kws['controller'].strip():
                        pairs.append(kws['controller'].strip())
                    if 'version' in kws  and kws['version'].strip():
                        pairs.append(kws['version'].strip())
                    if 'action' in kws  and kws['action'].strip():
                        pairs.append(kws['action'].strip())
                    elif url :
                        pairs.append(url)
                    url_path = "/"+"/".join(pairs)
                    return url_path
                    pass
                else:
                        
                    url_path = self.__template_path__.replace('{controller}',self.__controller_name__).replace("{version}",self.__version__)
                    return url_path + "/" + url.strip()
            else:
                url_path += '/' + self.__controller_name__
                if self.__version__:
                    url_path += '/' + self.__version__
                return url_path + "/"  + url.strip()
            
        if content:
            if format=='html':
                return HTMLResponse(content)
            elif format=='text':
                return PlainTextResponse(content)
        
        def get_path(caller_frame,view_path:str="",context:dict={},local2context:bool=True ):
            # caller_file = caller_frame.f_code.co_filename
            # caller_lineno = caller_frame.f_lineno
            caller_function_name = caller_frame.f_code.co_name
            caller_locals = caller_frame.f_locals
            caller_class = caller_locals.get("self", None).__class__
            caller_classname:str = caller_class.__name__
            caller_classname = caller_classname.replace("Controller","").lower()
            #caller_file = os.path.basename(caller.filename) 
            if local2context and not context:
                del caller_locals['self']
                context = caller_locals
            if not view_path:
                if self.__version__:
                    version_path = f"{self.__version__}/"
                else:
                    version_path = ""
                view_path = f"{caller_classname}/{version_path}{caller_function_name}.html" 
            return view_path,context
            
        caller_frame = inspect.currentframe().f_back
        view_path,context = get_path(caller_frame)
        template_path = os.path.join(self.__appdir__,"views")
        viewobj = _View(self._request,self._response, tmpl_path=template_path) 
        viewobj._templates.env.globals["url_for"] = url_for 
        return viewobj(view_path,context)
    
    async def getUploadFile(self,file:File):  
        
        if config.get("upload"):
            updir = config.get("upload")['dir'] or "uploads"
        else:
            updir = 'uploads'
        _save_dir = os.path.join(ROOT_PATH,updir) 
        if not os.path.exists(_save_dir):
            os.mkdir(_save_dir) 
        data = await file.read()
        ext = file.filename.split(".")[-1]
        md5_name = md5(data).hexdigest()
        if ext:
            md5_name+="."+ext
        save_file = os.path.join(_save_dir, md5_name) 
        if not os.path.exists(save_file): 
            f = open(save_file, 'wb') 
            f.write(data)
            f.close()
        return save_file
    async def _constructor(base_controller_class,request:Request,response:Response):  
        if not hasattr(request,'params') and request.method!='GET' and request.headers['content-type']=='application/json':
            request.params = await request.json()
        if not hasattr(request,'params'):
            request.params = {}
            if request.query_params:
                request.params = dict(request.query_params)
        base_controller_class._request:Request = request
        base_controller_class._response:Response = response 
        base_controller_class._cookies:Dict[str,str] = request.cookies.copy()
        base_controller_class._session = await  _sessionManager.initSession(request,response )
         
    async def _deconstructor(self,new_response:Response):  
        await _sessionManager.process_cookies(new_response,self._cookies,self._request.cookies)
        await _sessionManager.process(session =  self._session,response = new_response,request=self._request)
        pass