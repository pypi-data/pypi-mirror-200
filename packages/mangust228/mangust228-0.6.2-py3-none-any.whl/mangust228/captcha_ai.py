from loguru import logger
import asyncio 
import aiohttp
import requests
import time


class CaptchaAi:
    def __init__(self, token:str, async_:bool=False, threads:int=5):
        '''
        `token`  : is your <API_KEY> from captchaai.com
        `async_` : default False
        `threads`: default 5, working only with async mode 
        ''' 
        self.token = token
        self.async_=async_ 
        if async_:
            self.threads = threads
        self.url_solve_picture = 'https://ocr.captchaai.com/in.php'
        self.url_result = 'https://ocr.captchaai.com/res.php'

    def solve_picture(self, image:bytes, timeout:int=5, retries:int=3, **kwargs):
        '''
        `timeout`:  default 5
        `retries`:  default 3 How many retries to solve captcha.
        `phrase`:   0 - captcha contains one word
                    1 - captcha contains two or more words
        `regsense`: 0 - captcha in not case sensitive
                    1 - captcha is case sensitive
        `numeric`: 0 - not specified
                    1 - captcha contains only numbers
                    2 - captcha contains only letters
                    3 - captcha contains only numbers OR only letters
                    4 - captcha contains both numbers AND letters
        `calc`:     0 - not specified
                    1 - captcha requires calculation (e.g. type the result 4 + 8 = )
        `min_len`:  0 - not specified
                    1..20 - minimal number of symbols in captcha
        `max_len`:  0 - not specified
                    1..20 - maximal number of symbols in captcha
        `language`: 0 - not specified  
                    1 - Cyrillic captcha   
                    2 - Latin captcha  
        `lang`:     Language code. [See the list of supported languages](https://captchaai.com/api-docs.php#language).

        parameters `json`, `method` - doesn't support!
        '''
        data = self._get_picture_data(kwargs)
        if self.async_:
            return self._async_solve_picture(image, timeout, retries, data)
        return self._sync_solve_picture(image, timeout, retries, data)            


    def _get_picture_data(self, kwargs):
        return {'key':self.token,
                'method':'base64',
                'json':1, **kwargs}
    

    def _get_picture_params(self, key):
        return {'key':self.token,
                'action':'get',
                'json':1, 
                'id':key}

    def _sync_get_key_picture(self, image:bytes, data:dict) -> str:
        response = requests.post(self.url_solve_picture, 
                                 params=data, 
                                 files={'file':image})
        if response.status_code == 200 and response.json().get('status') == 1:
            return response.json().get('request')
        else: 
            raise Exception(f'Проблема с отправкой:\n'
                            f'{response.status_code = }\n{response.content}')


    def _sync_get_result(self, retries:int, timeout:int, key:str):
        params = self._get_picture_params(key)
        for _ in range(retries):
            time.sleep(timeout)
            response = requests.get(self.url_result,params=params)
            try:
                if response.status_code == 200 and response.json().get('status') == 1:
                    return response.json().get('request')
                else: 
                    logger.info(f'Проблемка с получение {response.content}')
            except Exception as e:
                logger.info(response.content)
                logger.warning(e)
        raise Exception(f'Не удалось получить ответ с трёх попыток {response.content = }')


    def _sync_solve_picture(self, image:bytes, timeout:int, retries:int, data: dict):
        key = self._sync_get_key_picture(image, data)
        logger.debug(f'{key = }')
        return self._sync_get_result(retries, timeout, key)



    async def _async_get_result(self, retries:int, timeout:int, key:str):
        async with aiohttp.ClientSession() as session:
            params = self._get_picture_params(key)
            for _ in range(retries):
                logger.debug(f'sleep')
                await asyncio.sleep(timeout)
                async with session.get(self.url_result, params=params) as resp:
                    if resp.status == 200:
                        result = await resp.json(content_type='text/html')
                        if result.get('status') != 1: 
                            raise Exception(f'Что то пошло не так {await resp.text()}')
                        return result.get('request')
                    else: 
                        logger.info(f'Проблемы при получении результата {resp.status} {await resp.text()}')

    @logger.catch
    async def _async_get_key_picture(self, image:bytes, data: dict):
        async with aiohttp.ClientSession() as session:
            form_data = aiohttp.FormData()
            for key, value in data.items():
                form_data.add_field(key, str(value))
            form_data.add_field('file', image)
            async with session.post(self.url_solve_picture, data=form_data) as resp:
                try:
                    if resp.status == 200: 
                        result = await resp.json(content_type='text/html')
                        logger.debug(f'{result = }')                
                        return result.get('request')
                    else: 
                        raise Exception(f'Не получилось послать... {resp.status = }, {await resp.text() = }')
                except Exception as e: 
                     logger.info(e)
                     logger.info(f'{await resp.text()}')



    async def _async_solve_picture(self, image:bytes, timeout:int, retries:int, data: dict):
        key = await self._async_get_key_picture(image, data)
        result = await self._async_get_result(retries, timeout, key)
        return result