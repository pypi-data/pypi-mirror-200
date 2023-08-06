import json
from deskaone_sdk_scrypt_v2.Client import Client
from deskaone_sdk_scrypt_v2.Exceptions import Error

class AntiCaptcha:
    
    def __init__(self, *args, **kwargs) -> None:
        """A Internal Requests.
        
        Basic Usage::

            AntiCaptcha(
                API_KEY = str || AntiCaptcha,
                URL_API = str || Server Scrypt,
                SECRET_KEY = str || Server Scrypt
            )
            
        params is Json/urlencode for POST/PUT or urlencode for GET
        """
        #RPC: str, secretKey: str, TimeOut: int, DEBUG: bool = False
        self._API_KEY, self._URL_API, self._SECRET_KEY = kwargs.get('API_KEY'), kwargs.get('URL_API'), kwargs.get('SECRET_KEY')
        if self._API_KEY is None:raise Error('RPC API Require')
        if self._URL_API is None:raise Error('API KEY ANTI CAPTCHA Require')
        if self._SECRET_KEY is None:raise Error('SECRET KEY WEB Require')
        self.client = Client(RPC = self._URL_API, secretKey = self._SECRET_KEY)
    
    def Params(self, *args, **kwargs):
        return dict(**kwargs, API_KEY = self._API_KEY)
                
    def getBalance(self, *args, **kwargs):
        self.client.Crypto.setData_FromString(json.dumps(self.Params(**dict(request = 'getBalance')), separators=(',', ':')))
        Params = json.dumps(dict(sub = f'{len(self.client.Crypto.getIv_to_Hex())}_{len(self.client.Crypto.getKey_to_Hex())}_{len(self.client.Crypto.encrypt_to_hex())}', data = self.client.Crypto.getKey_to_Hex() + self.client.Crypto.getIv_to_Hex() + self.client.Crypto.encrypt_to_hex()), separators=(',', ':'))
        return self.client.setRequest(App = 'AntiCaptcha', Params = Params, Command = 'INTERNAL')
    
    def createTask(self, *args, **kwargs):
        """A Internal Requests.
        
        Basic Usage::

            createTask(
                type = str || ex : RecaptchaV2TaskProxyless,
                websiteURL = str || ex : http://makeawebsitehub.com/recaptcha/test.php,
                websiteKey = str || ex : 6LfI9IsUAAAAAKuvopU0hfY8pWADfR_mogXokIIZ
            )
            
        params is Json/urlencode for POST/PUT or urlencode for GET
        """
        self.client.Crypto.setData_FromString(json.dumps(self.Params(**dict(request = 'createTask', **kwargs)), separators=(',', ':')))
        Params = json.dumps(dict(sub = f'{len(self.client.Crypto.getIv_to_Hex())}_{len(self.client.Crypto.getKey_to_Hex())}_{len(self.client.Crypto.encrypt_to_hex())}', data = self.client.Crypto.getKey_to_Hex() + self.client.Crypto.getIv_to_Hex() + self.client.Crypto.encrypt_to_hex()), separators=(',', ':'))
        return self.client.setRequest(App = 'AntiCaptcha', Params = Params, Command = 'INTERNAL')
    
    def getTaskResult(self, taskId: int):
        self.client.Crypto.setData_FromString(json.dumps(self.Params(**dict(request = 'getTaskResult', taskId = taskId)), separators=(',', ':')))
        Params = json.dumps(dict(sub = f'{len(self.client.Crypto.getIv_to_Hex())}_{len(self.client.Crypto.getKey_to_Hex())}_{len(self.client.Crypto.encrypt_to_hex())}', data = self.client.Crypto.getKey_to_Hex() + self.client.Crypto.getIv_to_Hex() + self.client.Crypto.encrypt_to_hex()), separators=(',', ':'))
        return self.client.setRequest(App = 'AntiCaptcha', Params = Params, Command = 'INTERNAL')
    
    def getQueueStats(self, queueId: int):
        self.client.Crypto.setData_FromString(json.dumps(self.Params(**dict(request = 'getQueueStats', queueId = queueId)), separators=(',', ':')))
        Params = json.dumps(dict(sub = f'{len(self.client.Crypto.getIv_to_Hex())}_{len(self.client.Crypto.getKey_to_Hex())}_{len(self.client.Crypto.encrypt_to_hex())}', data = self.client.Crypto.getKey_to_Hex() + self.client.Crypto.getIv_to_Hex() + self.client.Crypto.encrypt_to_hex()), separators=(',', ':'))
        return self.client.setRequest(App = 'AntiCaptcha', Params = Params, Command = 'INTERNAL')
    
    def reportIncorrectImageCaptcha(self, taskId: int):
        self.client.Crypto.setData_FromString(json.dumps(self.Params(**dict(request = 'reportIncorrectImageCaptcha', taskId = taskId)), separators=(',', ':')))
        Params = json.dumps(dict(sub = f'{len(self.client.Crypto.getIv_to_Hex())}_{len(self.client.Crypto.getKey_to_Hex())}_{len(self.client.Crypto.encrypt_to_hex())}', data = self.client.Crypto.getKey_to_Hex() + self.client.Crypto.getIv_to_Hex() + self.client.Crypto.encrypt_to_hex()), separators=(',', ':'))
        return self.client.setRequest(App = 'AntiCaptcha', Params = Params, Command = 'INTERNAL')
    
    def reportIncorrectRecaptcha(self, taskId: int):
        self.client.Crypto.setData_FromString(json.dumps(self.Params(**dict(request = 'reportIncorrectRecaptcha', taskId = taskId)), separators=(',', ':')))
        Params = json.dumps(dict(sub = f'{len(self.client.Crypto.getIv_to_Hex())}_{len(self.client.Crypto.getKey_to_Hex())}_{len(self.client.Crypto.encrypt_to_hex())}', data = self.client.Crypto.getKey_to_Hex() + self.client.Crypto.getIv_to_Hex() + self.client.Crypto.encrypt_to_hex()), separators=(',', ':'))
        return self.client.setRequest(App = 'AntiCaptcha', Params = Params, Command = 'INTERNAL')
    
    def reportCorrectRecaptcha(self, taskId: int):
        self.client.Crypto.setData_FromString(json.dumps(self.Params(**dict(request = 'reportCorrectRecaptcha', taskId = taskId)), separators=(',', ':')))
        Params = json.dumps(dict(sub = f'{len(self.client.Crypto.getIv_to_Hex())}_{len(self.client.Crypto.getKey_to_Hex())}_{len(self.client.Crypto.encrypt_to_hex())}', data = self.client.Crypto.getKey_to_Hex() + self.client.Crypto.getIv_to_Hex() + self.client.Crypto.encrypt_to_hex()), separators=(',', ':'))
        return self.client.setRequest(App = 'AntiCaptcha', Params = Params, Command = 'INTERNAL')
    
    def reportIncorrectHcaptcha(self, taskId: int):
        self.client.Crypto.setData_FromString(json.dumps(self.Params(**dict(request = 'reportIncorrectHcaptcha', taskId = taskId)), separators=(',', ':')))
        Params = json.dumps(dict(sub = f'{len(self.client.Crypto.getIv_to_Hex())}_{len(self.client.Crypto.getKey_to_Hex())}_{len(self.client.Crypto.encrypt_to_hex())}', data = self.client.Crypto.getKey_to_Hex() + self.client.Crypto.getIv_to_Hex() + self.client.Crypto.encrypt_to_hex()), separators=(',', ':'))
        return self.client.setRequest(App = 'AntiCaptcha', Params = Params, Command = 'INTERNAL')