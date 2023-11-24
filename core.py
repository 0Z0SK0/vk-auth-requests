import aiohttp
import re
import time

VK_API_VERSION = "5.207"

class Core(object):
    def __init__(self):
        self.headers = {
            "User-Agent": ""
        }

        self.session = aiohttp.ClientSession(headers=self.headers)

        self.access_token = None
        self.anonymous_token = None
        self.login_sid = None

    async def handleError(self, response):
        try:
            if (response["type"] == "error"):
                error_code = response["error"]["error_code"]

                # Captcha needed
                if (error_code == 14):
                    captcha_sid = response["error"]["captcha_sid"]
                    captcha_img = response["error"]["captcha_img"]
                    captcha_ts = response["error"]["captcha_ts"]
                    captcha_attempt = response["error"]["captcha_attempt"]

                    # here must be place captcha solver (2captcha or another)
                    captcha_key = input("key: ")

                    return {
                        "response": False,
                        "error": "captcha",
                        "captcha_sid": captcha_sid,
                        "captcha_img": captcha_img,
                        "captcha_ts": captcha_ts,
                        "captcha_attempt": captcha_attempt,
                        "captcha_key": captcha_key
                    }
                
                # Слишком много запросов в секунду
                elif (error_code == 6):
                    return {
                        "response": False,
                        "error": "toomanyrequests"
                    }
                
                # Внутренняя ошибка сервера
                elif (error_code == 10):
                    return {
                        "response": False,
                        "error": "internalerror"
                    }

                else:
                    return {
                        "response": False,
                        "error": response['error_info']
                    }
                
            if (response['type'] == "captcha"):
                captcha_sid = response["error"]["captcha_sid"]
                captcha_img = response["error"]["captcha_img"]
                captcha_ts = response["error"]["captcha_ts"]
                captcha_attempt = response["error"]["captcha_attempt"]

                # here must be place captcha solver (2captcha or another)
                captcha_key = input("key: ")

                return {
                    "response": False,
                    "error": "captcha",
                    "captcha_sid": captcha_sid,
                    "captcha_img": captcha_img,
                    "captcha_ts": captcha_ts,
                    "captcha_attempt": captcha_attempt,
                    "captcha_key": captcha_key
                }
        except Exception as e:
            return {
                "response": True
            }

    async def performRequest(self, type, url, data={}, headers=None):
        if (headers is None):
            _headers = self.headers
        else:
            _headers = headers

        if (type == "POST"):
            async with self.session.post(url, data=data, headers=_headers) as response:
                _response = await response.json()
                resp = await self.handleError(_response)
                try:
                    if (resp["response"] == False):
                        if (resp["error"] == "captcha"):
                            data["captcha_sid"]     = resp["captcha_sid"],
                            data["captcha_img"]     = resp["captcha_img"],
                            data["captcha_ts"]      = resp["captcha_ts"],
                            data["captcha_attempt"] = resp["captcha_attempt"]
                            data["captcha_key"]     = resp["captcha_key"]
                            
                            return await self.performRequest(type, url, data, _headers)
                        
                        elif (resp["error"] == "toomanyrequests"):
                            time.sleep(1)
                            return await self.performRequest(type, url, data, _headers)
                        
                        elif (resp["error"] == "internalerror"):
                            return await self.performRequest(type, url, data, _headers)
                    else:
                        _response['response'] = True
                        return _response
                except Exception:
                    _response['response'] = False
                    return _response
                
        elif (type == "GET"):
            async with self.session.get(url, headers=_headers) as response:
                _response = await response.json()
                resp = await self.handleError(_response)

                if (resp["response"] == False):
                    if (resp["error"] == "captcha"):
                        data["captcha_sid"] = resp["captcha_sid"],
                        data["captcha_img"] = resp["captcha_img"],
                        data["captcha_ts"] = resp["captcha_ts"],
                        data["captcha_attempt"] = resp["captcha_attempt"]
                        data["captcha_key"] = resp["captcha_key"]

                        return await self.performRequest(type, url, data, _headers)
                    
                    elif (resp["error"] == "toomanyrequests"):
                        time.sleep(1)
                        return await self.performRequest(type, url, data, _headers)
                    
                    elif (resp["error"] == "internalerror"):
                        return await self.performRequest(type, url, data, _headers)
                else:
                    return _response

    async def getAccessToken(self):
        _headers = self.headers
        _headers["Origin"] = "https://id.vk.com"
        _headers["Referer"] = "https://id.vk.com/"

        _data = {
            "version": "1",
            "app_id": "7344294",
            "access_token": "" 
        }

        res = await self.performRequest("POST", "https://login.vk.com/?act=web_token", _data, _headers)
        if (res['type'] == "okay"):
            return {
                "response": True,
                "access_token": res['data']['access_token']
            }
            
        elif (res['type'] == "error"):
            return {
                "response": False,
                "error": res['error_code']
            }

    async def getAuthTokens(self):
        _url = "https://id.vk.com/qr_auth?scheme=bright_light&app_id=7913379&origin=https%3A%2F%2Fvk.com"
        async with self.session.get(_url, headers=self.headers) as response:
            _response = await response.text()
            
            # Find access token
            match = re.search(r'access_token":"([^"]+)"', _response)
            access_token = match.group(1) if match and match.group(1) else None

            # Find anonymous token
            match = re.search(r'anonymous_token":"([^"]+)"', _response)
            anonymous_token = match.group(1) if match and match.group(1) else None

            if access_token is None or anonymous_token is None:
                return {
                    "response": False
                }
            else:
                return {
                    "response": True,
                    "access_token": access_token,
                    "anonymous_token": anonymous_token
                }