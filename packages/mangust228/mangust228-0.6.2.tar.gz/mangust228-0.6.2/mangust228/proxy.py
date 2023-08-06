from datetime import date, timedelta, datetime
import requests
from loguru import logger
import pandas as pd 
import json
from pydantic import BaseModel 


class ProxyManager:
    def __init__(self, token:int, url: str):
        '''
        url - адрес по которому посылать запрос для получения списка актуальных прокси
        token - токен для опознания на сервере
        '''
        self.url = url 
        self.token = token 
        self.types = {'string', 'dict[str,str]','playwright'}

    
    def get(self, request_type='string', expire:str | date | datetime=None):
        '''
        Возвращает список актуальных прокси    

        type: str : ['string', 'dict[str,str]','playwright']
        expire: str | date | datetime 

        ---
        `type` может быть следующих значений:
          - 'string', вернет в формате:   
            [{"http" : "http://user:pass@127.0.0.1:8000", "https":"https://user:pass@127.0.0.1:8000}, ...]
          - 'dict[str,str] вернет в формате:
            [{"server":"http://127.0.0.1:8000","username":"user","password":"pass"}...]
          - 'playwright'
            [{"proxy":{
              "server":"http://127.0.0.1:8000","username":"user","password":"pass"}
              },...]
        ---

        `expire` - до какой даты, если не указано, то вернет, те что работают до завтра
        передавать либо объект date | datetime, либо строку формата : "2023-02-15"        
        '''
        if request_type not in self.types:
            raise ValueError(f'type must be {self.types}')
        expire = self._check_expire(expire)
        return self._request(expire, request_type)


    def get_full(self, path:str = None):
        '''
        Возвращает все прокси которые есть на сервере
        '''
        resp = requests.get(url=f'{self.url}/full/', params={'token':self.token})
        if resp.status_code == 200:
            if path is None:
                logger.info(json.dumps(resp.json().get('data'), indent=4))
            else:
                pd.DataFrame(resp.json().get('data')).to_csv(path, index=False)
        else: # status_code != 200
            raise Exception(f'[{resp.status_code}] {resp.content}')


    def post(self, data: list[dict]=None, path:str=None):
        '''
        Опубликовать новые прокси
        Указывается либо `path` либо `data`, вместе нельзя и ничего указывать нельзя!

        `path`:str - Путь до файла (формат xlsx, csv), проверить на наличие соответствующих колонок  

        `data`:list[dict] - Список словарей, должен быть следующего формата:

        ```python
        data = [
        {"server":"127.0.0.1"}, 
        {"username":"user"},
        {"password":"pass"}, 
        {"port":8000},
        {"expire":"2023-02-23"} # Дата до которой прокси работает
        {"service":"example.service.ru"} # Опционально
        ]
        proxies = GetterProxy(token)
        proxies.post(data)
        ```
        '''
        if data is None and path is not None: 
            data = self._get_data_to_post_request(path)
        elif data is not None and path is None: 
            [_PostProxy(datum) for datum in data]
        else: 
            raise ValueError(f'you can set data OR path.')
        [_PostProxy(**datum) for datum in data]
        self._request_post(data)

    def delete(self, id):
        '''Удаляет прокси с сервера по id'''
        resp = requests.delete(self.url, params={'token':self.token, 'id':id})
        logger.info(resp.status_code)
        if resp.status_code == 200 or resp.status_code == 201:
            logger.info(f'Succesful delete {resp.json()}')
        else: 
            raise Exception(f'[{resp.status_code}] {resp.json()}')
        
    def update(self, data:dict[str,str|int]):
        '''
        Обновляет прокси на сервере, пример словаря:
        ```python
        data = {
            "id":4, 
            # тут параметры которые надо изменить, например: 
            "service":"new_service",
            ...
        }
        ```
        '''
        resp = requests.put(url=self.url, params={'token':self.token}, data=json.dumps(data))
        if resp.status_code == 200 or resp.status_code == 201:
            logger.info(f'Succesful update {resp.json()}')
        else: 
            raise Exception(f'[{resp.status_code}] {resp.json()}')

    @staticmethod
    def _get_data_to_post_request(path: str):
        if path is not None: 
            type_fp = path.split('.')[-1]
        if type_fp == 'csv':
            data = pd.read_csv(path).to_dict('records')
        elif type_fp == 'xlsx':
            data = pd.read_excel(path, index_col=False).to_dict('records')
        else: # type_fp is not 'csv' and 'xlsx'
            raise TypeError(f'type file can be only `.xlsx` or `.csv`')
        return data
    
    def _request_post(self, data):
        data = {
            'token':self.token,
            'data': data
        }
        resp = requests.post(self.url, data=json.dumps(data))
        if resp.status_code == 200 or resp.status_code == 201:
            logger.info(resp.content)
        else:
            raise Exception(f'[{resp.status_code}] {resp.json()}')

    def _request(self, expire, request_type):
        params = self._make_params(expire, request_type)
        resp =  requests.get(self.url, params=params)
        if resp.status_code == 200: 
            logger.info(f'Получены прокси: {len(resp.json().get("data"))} шт')
            return resp.json().get('data')
        elif resp.status_code == 204:
            raise Exception('Нет прокси актуальных...') 
        else:
            raise Exception(f'[{resp.status_code}] {resp.content}')


    @staticmethod
    def _check_expire(expire):
        if isinstance(expire, date | datetime):
            return expire.strftime('%Y-%m-%d')
        if expire is None:
            return (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
        try: 
            return datetime.strptime(expire, '%Y-%m-%d').strftime('%Y-%m-%d')
        except:
            raise ValueError(f'expire must be in format 2023-02-15')      


    def _make_params(self, expire, request_type):
        return {
            'token':self.token,
            'expire': expire,
            'type':request_type
        }


class _PostProxy(BaseModel):
    server: str 
    port: int 
    password: str
    username: str 
    expire: str | date | datetime
    service: str | None = None 
