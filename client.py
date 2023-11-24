from core import Core

import re

VK_API_VERSION = "5.207"

class Client(object):
    async def getAuthFlow(self, core, login, access_token):
        _url = "https://api.vk.com/method/auth.validateAccount?v=" + VK_API_VERSION + "&client_id=7913379"

        _data = {
            "login": login,
            "sid": "",
            "client_id": "7913379",
            "device_id": "",
            "auth_token": access_token,
            "super_app_token": "",
            "supported_ways": "push,email,passkey",
            "is_switcher_flow": "false",
            "access_token": ""
        }

        res = await core.performRequest("POST", _url, _data)

        if (res['response'] == False):
            return {
                "response": False
            }
        
        else:
            self.login_sid = res['response']['sid']
                
            return res['response']['flow_name']

    async def authPassword(self, core, login, password):
        tokens = await core.getAuthTokens()
        if tokens['response'] == True:
            _url = "https://login.vk.com/?act=connect_authorize"

            _headers = {
                "Origin": "https://id.vk.com",
                "Referer": "https://id.vk.com/"
            }

            _data = {
                "username": login,
                "password": password,
                "auth_token": tokens['access_token'],
                "sid": "",
                "uuid": "",
                "v": VK_API_VERSION,
                "device_id": "",
                "service_group": "",
                "agreement_hash": "",
                "expire": "0",
                "save_user": "0",
                "to": "",
                "version": "1",
                "app_id": "7913379"
            }

            res = await core.performRequest("POST", _url, _data, _headers)
            print(res)
            if (res['response']):
                self.login_sid = res['response']['sid']
                    
                return res['response']['flow_name']
            
            else:
                return {
                    "response": False
                }

                # successful
                if (res['type'] == "okay"):
                    print('authed')

                elif (res['type'] == "error"):
                    if (res['error_code'] == "incorrect_password"):
                        # wrong password
                        pass