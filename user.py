import aiohttp
import re

class User():
    async def getInfo(self, core, access_token):
        _url = "https://api.vk.com/method/account.getProfileInfo"

        _data = {
            "lang": "0",
            "v": "5.190",
            "access_token": access_token,
            "showSpinner": "true",
            "vkui": "1"
        }

        response = await core.performRequest("POST", _url, _data)

        if (response['response'] == False):
            return {
                "response": False
            }
        
        else:
            print(response)

    async def reactivateAccount(self, core, access_token):
        _url = "https://api.vk.com/method/account.reactivate"

        _data = {
            "lang": "0",
            "v": "5.190",
            "access_token": access_token,
            "showSpinner": "true",
            "vkui": "1"
        }

        response = await core.performRequest("POST", _url, _data)

        if (response['response'] == False):
            return {
                "response": False
            }
        
        else:
            print(response)

    async def changePassword(self, core, access_token, old_password, new_password):
        _url = "https://api.vk.com/method/settings.changePasswordStart"

        _data = {
            "lang": "0",
            "v": "5.190",
            "access_token": access_token,
            "vkui": "1"
        }

        response = await core.performRequest("POST", _url, _data)
        print(response)
        '''
        if (response['response'] == False):
            return {
                "response": False
            }
        
        else:
            _url = "https://api.vk.com/method/cua.checkPassword"

            _data = {
                "lang": "0",
                "v": "5.190",
                "access_token": access_token,
                "session": session,
                "password": old_password,
                "vkui": "1"
            }

            response = await core.performRequest("POST", _url, _data)

            if (response['response'] == False):
                return {
                    "response": False
                }
            
            else:
                _url = "https://api.vk.com/method/settings.doChangePassword"

                _data = {
                    "lang": "0",
                    "v": "5.190",
                    "access_token": access_token,
                    "app_id": "7344294",
                    "new_password": new_password,
                    "hash": hash,
                    "reset_session": "0",
                    "vkui": "1"
                }

                response = await core.performRequest("POST", _url, _data)

                if (response['response'] == False):
                    return {
                        "response": False
                    }
                
                else:
                    _url = "https://login.vk.com/?act=connect_exchange_token"

                    _data = {
                        "token": "0",
                        "hash": hash,
                        "version": "1",
                        "app_id": "7344294"
                    }

                    response = await core.performRequest("POST", _url, _data)

                    if (response['response'] == False):
                        return {
                            "response": False
                        }
                    
                    else:
        '''