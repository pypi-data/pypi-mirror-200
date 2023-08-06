from deskaone_sdk_scrypt_v2.Internal import API, Internal
from deskaone_sdk_scrypt_v2.Exceptions import Error
from deskaone_sdk_scrypt_v2.Utils import Crypto
from typing import Tuple


class Client:
    
    def __init__(self, *args, **kwargs) -> None:
        """A Internal Requests.
        
        Basic Usage::

            ClientV2(
                RPC         = str,
                secretKey   = bool (Optional)
            )
            
        params 
        """
        self._RPC, self._secretKey = kwargs.get('RPC'), kwargs.get('secretKey')
        if self._RPC is None:raise Error('RPC API Require')
        if self._secretKey is None:raise Error('secretKey Require')
        self._CR = Crypto.AES()
        self._CR.randomIv()
        self._CR.randomKey()
        self._api    = API(self._secretKey, self._RPC)
    
    @property
    def Crypto(self):
        return self._CR
    
    def setRequest(self, *args, **kwargs) -> Tuple[bool, dict]:
        """A Internal Requests.
        
        Basic Usage::

            setRequest(
                App     = str | Credits or getProxy or addProxy or getVersion or getScrypt or Coinbase or Bprogrammers or PlayFabapi or Viker or Email or AntiCaptcha or Other or Zebedee,
                Params  = str,
                Command = str | INTERNAL or EXTERNAL,
                IpPort  = str | None, example 127.0.0.1:8080
                TypeIp  = str | HTTP | HTTPS | SOCKS4 | SOKCS5 | None, example SOCKS5
                TimeOut = int | if Command INTERNAL
            )
            
        params is 
        """
        try:
            if kwargs.get('App') == 'Credits':Result = self._api.Credits(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'getProxy':Result = self._api.getProxy(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'addProxy':Result = self._api.addProxy(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'getVersion':Result = self._api.getVersion(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'getScrypt':Result = self._api.getScrypt(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'Coinbase':Result = self._api.Coinbase(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'Bprogrammers':Result = self._api.Bprogrammers(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'PlayFabapi':Result = self._api.PlayFabapi(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'Viker':Result = self._api.Viker(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'Email':Result = self._api.Email(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'AntiCaptcha':Result = self._api.AntiCaptcha(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'Zebedee':Result = self._api.Zebedee(Params=kwargs.get('Params'))
            elif kwargs.get('App') == 'Test':Result = self._api.Test(Params=kwargs.get('Params'))
            else:Result = self._api.sender(Params=kwargs.get('Params'))
            if Result.get('status') is True:
                if kwargs.get('Command').upper() == 'EXTERNAL':call_back = True, Result
                elif kwargs.get('Command').upper() == 'INTERNAL':call_back = True, Internal(URL=dict(Result.get('data')).get('url'), PARAMS=dict(Result.get('data')).get('data'), HEADER=dict(Result.get('data')).get('headers')).Setup(IpPort=kwargs.get('IpPort'), Type=kwargs.get('TypeIp'), Mode=dict(Result.get('data')).get('methods'), TimeOut=60 if kwargs.get('TimeOut') is None else kwargs.get('TimeOut'))
                else:call_back = False, dict()
            else:call_back = False, Result
            return call_back
        except Error as e:raise Error(str(e))
        except Exception as e:raise Exception(str(e))
        