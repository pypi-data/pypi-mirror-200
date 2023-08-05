import json
from requests.exceptions import ConnectionError, ConnectTimeout, ProxyError, ReadTimeout, JSONDecodeError, TooManyRedirects
import requests
from deskaone_sdk_scrypt_v2.Exceptions import Error

class Internal:
    
    def __init__(self, *args, **kwargs) -> None:
        """A Internal Requests.
        
        Basic Usage::

            Internal(
                URL     = str,
                PARAMS  = str,
                HEADER  = dict
            )
            
        params is Json/urlencode for POST/PUT or urlencode for GET
        """
        self.URL        = kwargs.get('URL')
        self.PARAMS     = kwargs.get('PARAMS')
        self.HEADER     = kwargs.get('HEADER')
        self.Session    = requests.Session()
    
    @property
    def setProxy(self):
        if self.Type.upper() == 'HTTP' or self.Type.upper() == 'HTTPS':Proxies = dict(http=f"http://{self.IpPort}", https=f"http://{self.IpPort}")
        elif self.Type.upper() == 'SOCKS4':Proxies = dict(http=f"socks4://{self.IpPort}", https=f"socks4://{self.IpPort}")
        elif self.Type.upper() == 'SOCKS5':Proxies = dict(http=f"socks5://{self.IpPort}", https=f"socks5://{self.IpPort}")
        else:Proxies = dict(http=f"http://{self.IpPort}", https=f"http://{self.IpPort}")
        self.Session.proxies     = Proxies
    
    @staticmethod
    def __ParseResult__(Result: any):
        try:return Result if type(Result) == dict else dict(json.loads(Result))
        except:
            try:return Result if type(Result) == str else str(Result)
            except:return dict()
    
    def Setup(self, *args, **kwargs) -> dict:
        """A Internal Requests.
        
        Basic Usage::

            Internal(
                URL     = str,
                PARAMS  = str | JSON | URLENCODE,
                HEADER  = dict
            ).Setup(
                IpPort  = str | None, example 127.0.0.1:8080
                Type    = str | HTTP | HTTPS | SOCKS4 | SOKCS5 | None, example SOCKS5 
                Mode    = str | POST | GET | PUT, | default GET
                TimeOut = int | default 15 seconds
            )
            
        params is Json/urlencode for POST/PUT or urlencode for GET
        
        IpPort format 127.0.0.1:8000
        
        Type SOCKS5/SOCKS4/HTTP/HTTPS  default HTTP
        
        Mode POST/PUT/GET default GET
        
        Basic Return::

            return text: str
            
        """
        if kwargs.get('IpPort') is not None and kwargs.get('Type') is not None:
            self.IpPort = str(kwargs.get('IpPort'))
            self.Type   = str(kwargs.get('Type'))
            self.setProxy
        self.Mode       = 'GET' if kwargs.get('Mode') is None else kwargs.get('Mode')
        self.TimeOut    = 15 if kwargs.get('TimeOut') is None else kwargs.get('TimeOut')
        try:
            if self.Mode == 'POST':Result = self.Session.post(self.URL, data=self.PARAMS, headers=self.HEADER, timeout=self.TimeOut)
            elif self.Mode == 'PUT':Result = self.Session.put(self.URL, data=self.PARAMS, headers=self.HEADER, timeout=self.TimeOut)
            else:
                if self.PARAMS is None:Result = self.Session.get(self.URL, headers=self.HEADER, timeout=self.TimeOut)
                else:Result = self.Session.get(self.URL, params=self.PARAMS, headers=self.HEADER, timeout=self.TimeOut)
            self.Session.close()
            return dict(result  = self.__ParseResult__(Result.text), code = Result.status_code)
        except ProxyError as e:raise Error(f'ProxyError')
        except ConnectTimeout as e:raise Error(f'ConnectTimeout')
        except ConnectionError as e:raise Error(f'ConnectionError')
        except ReadTimeout as e:raise Error(f'ReadTimeout')
        except JSONDecodeError:raise Error(f'JSONDecodeError')
        except TooManyRedirects as e:raise Error(f'TooManyRedirects')
        except Exception as e:raise Exception(str(e))