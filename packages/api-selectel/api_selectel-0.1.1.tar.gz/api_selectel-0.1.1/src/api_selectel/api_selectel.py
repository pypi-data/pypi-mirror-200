import requests
import json
from enum import Enum
from jinja2 import Template
from typing import Tuple

RECORDS_TYPE=["SOA", "NS", "A", "AAAA", "CNAME", "SRV", "MX", "TXT", "SPF"]

class Request_types(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    DELETE = 'DELETE'


class Api_Selectel():

    def __init__(self, token: str, url_basepart: str = 'https://api.selectel.ru') -> None:
        self.token = token
        self.headers = {'X-Token': self.token, 'content-type': 'application/json'}
        self.url_basepart = url_basepart
        self.url_api_dns_suffix = '/domains/v1/'
        self.url_template_base = '{{ url_basepart }}{{ url_suffix }}'
        self.requests_description = {"domain_list": {"url_suffix_template": self.url_api_dns_suffix, "rtype": Request_types.GET, "params": {'limit': 'int(value)', 'offset': 'int(value)', 'show_ips': 'str(value).lower()'}},
                                     "domain_create": {"url_suffix_template": self.url_api_dns_suffix, "rtype": Request_types.POST, "body": {'bind_zone': 'str(value)', 'name': 'str(value)'}},
                                     "domain_delete": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_id }}', "rtype": Request_types.DELETE},
                                     "domain_get_by_id": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_id }}', "rtype": Request_types.GET},
                                     "domain_update": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_id }}', "rtype": Request_types.PATCH, "body": {'tags': 'value'}},
                                     "domain_export": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_id }}/export', "rtype": Request_types.GET},
                                     "domain_get_by_name": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_name }}', "rtype": Request_types.GET},
                                     "records_list_by_domain_id": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_id }}/records/', "rtype": Request_types.GET, "params": {'limit': 'int(value)', 'offset': 'int(value)'}},
                                     "records_create": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_id }}/records/', "rtype": Request_types.POST, "body": {'content': 'str(value)', 'email': 'str(value)', 'name': 'str(value)', 'port': 'int(value)', 'priority': 'int(value)', 'target': 'str(value)', 'ttl': 'int(value)', 'type': 'str(value)', 'weight': 'int(value)'}},
                                     "records_delete": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_id }}/records/{{record_id}}', "rtype": Request_types.DELETE},
                                     "records_get": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_id }}/records/{{record_id}}', "rtype": Request_types.GET},
                                     "records_update": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_id }}/records/{{record_id}}', "rtype": Request_types.PUT, "body": {'content': 'str(value)', 'email': 'str(value)', 'name': 'str(value)', 'port': 'int(value)', 'priority': 'int(value)', 'target': 'str(value)', 'ttl': 'int(value)', 'type': 'str(value)', 'weight': 'int(value)'}},
                                     "records_list_by_domain_name": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_name }}/records/', "rtype": Request_types.GET, "params": {'limit': 'int(value)', 'offset': 'int(value)'}},
                                     "records_batch_update": {"url_suffix_template": self.url_api_dns_suffix + '{{ domain_name }}/records/batch_update', "rtype": Request_types.PATCH, "body": {'create': 'value', 'delete': 'value', 'update': 'value'}},
                                     "ptr_list": {"url_suffix_template": self.url_api_dns_suffix + '/ptr/', "rtype": Request_types.GET, "params": {'limit': 'int(value)', 'offset': 'int(value)'}},
                                     "ptr_create": {"url_suffix_template": self.url_api_dns_suffix + '/ptr/', "rtype": Request_types.POST, "body": {'content': 'str(value)', 'ip': 'str(value)'}},
                                     "ptr_delete": {"url_suffix_template": self.url_api_dns_suffix + '/ptr/{{ ptr_id }}', "rtype": Request_types.DELETE},
                                     "ptr_get": {"url_suffix_template": self.url_api_dns_suffix + '/ptr/{{ ptr_id }}', "rtype": Request_types.GET},
                                     "ptr_update": {"url_suffix_template": self.url_api_dns_suffix + '/ptr/{{ ptr_id }}', "rtype": Request_types.PUT, "body": {'content': 'str(value)', 'ip': 'str(value)'}},
                                     "tags_list": {"url_suffix_template": self.url_api_dns_suffix + '/tags/', "rtype": Request_types.GET},
                                     "tags_create": {"url_suffix_template": self.url_api_dns_suffix + '/tags/', "rtype": Request_types.POST, "body": {'name': 'str(value)', 'domains': 'value'}},
                                     "tags_delete": {"url_suffix_template": self.url_api_dns_suffix + '/tags/{{ tag_id }}', "rtype": Request_types.DELETE},
                                     "tags_get": {"url_suffix_template": self.url_api_dns_suffix + '/tags/{{ tag_id }}', "rtype": Request_types.GET},
                                     "tags_update": {"url_suffix_template": self.url_api_dns_suffix + '/tags/{{ tag_id }}', "rtype": Request_types.PUT, "body": {'name': 'str(value)', 'domains': 'value'}}}

    def make_request(func):
        def _wrapper(self, **kwargs):
            caller_name = func.__name__
            request_options = self.requests_description[caller_name]
            url_suffix_template = request_options['url_suffix_template']
            url_suffix = Template(url_suffix_template).render(domain_id=kwargs.get('domain_id', ''),
                                                              domain_name=kwargs.get('domain_name', ''),
                                                              record_id=kwargs.get('record_id', ''),
                                                              ptr_id=kwargs.get('ptr_id', ''),
                                                              tag_id=kwargs.get('tag_id', ''))
            url = Template(self.url_template_base).render(url_basepart=self.url_basepart, url_suffix=url_suffix)
            params = dict()
            body = dict()
            if (len(kwargs) != 0) and ('params' in request_options):
                params_list = request_options['params']
                params_name_list = params_list.keys()
                for keyname in kwargs:
                    if (keyname in params_name_list):
                        value = kwargs[keyname]
                        if value is not None:
                            params[keyname] = eval(params_list[keyname])
            if (len(kwargs) != 0) and ('body' in request_options):
                body_items = request_options['body']
                body_items_name_list = body_items.keys()
                for keyname in kwargs:
                    if (keyname in body_items_name_list):
                        value = kwargs[keyname]
                        if value is not None:
                            body[keyname] = eval(body_items[keyname])
            rtype = request_options['rtype']
            return self.request(url=url, rtype=rtype, params=params, body=body)
        return _wrapper

    def request(self, url: str, rtype=Request_types.GET, params: str = '', body: str = '', return_json: bool = True) -> Tuple[str, int, str]:
        responce=requests.request(method=str(rtype.value),url=url, headers=self.headers, params=params, json=body)
        text = ''
        status = int(responce.status_code)
        headers = responce.headers
        if (status == 200) or (status == 204):
            text = responce.text
            if (headers.get('content-type','') == "application/json"):
                text = json.loads(text)
        return (text, status, headers)

    @make_request
    def domain_list(self, limit: int = 1000, offset: int = 0, show_ips: bool = False) -> Tuple[str, int, str]:
        '''
        Получить список своих доменов
        '''
        pass

    @make_request
    def domain_create(self, bind_zone: str, name: str) -> Tuple[str, int, str]:
        '''
        Создать домен
        '''
        pass

    @make_request
    def domain_delete(self, domain_id: int) -> Tuple[str, int, str]:
        '''
        Удалить домен
        '''
        pass

    @make_request
    def domain_get_by_id(self, domain_id: int) -> Tuple[str, int, str]:
        '''
        Получить информацию о заданном домене по id
        '''
        pass

    @make_request
    def domain_update(self, domain_id: int, tags) -> Tuple[str, int, str]:
        '''
        Обновить домен
        '''
        pass

    @make_request
    def domain_export(self, domain_id: int) -> Tuple[str, int, str]:
        '''
        Получить файл зоны указанного домена в формате BIND
        '''
        pass

    @make_request
    def domain_get_by_name(self, domain_name: str) -> Tuple[str, int, str]:
        '''
        Получить информацию о заданном домене по имени
        '''
        pass

    def domain_id(self, domain_name: str) -> int:
        '''
        Возвращает id домена по его имени
        '''
        r, s, _ = self.domain_get_by_name(domain_name=domain_name)
        if s == 200:
            return int(r['id'])
        return 0

    def domain_name(self, domain_id: int) -> str:
        '''
        Возвращает имя домена по его id
        '''
        r, s, _ = self.domain_get_by_id(domain_id=domain_id)
        if s == 200:
            return r['name']
        return ''

    @make_request
    def records_list_by_domain_id(self, domain_id: int, limit: int = 1000, offset: int = 0) -> Tuple[str, int, str]:
        '''
        Получить список записей, принадлежащих заданному домену по id
        '''
        pass

    @make_request
    def records_create(self, domain_id: int, content: str, email: str, name: str, port: int, priority: int, target: str, ttl: int, type: str, weight: int) -> Tuple[str, int, str]:
        '''
        Создать ресурсную запись для заданного домена
        '''
        pass

    @make_request
    def records_delete(self, domain_id: int, record_id: int) -> Tuple[str, int, str]:
        '''
        Удалить ресурсную запись
        '''
        pass

    @make_request
    def records_get(self, domain_id: int, record_id: int) -> Tuple[str, int, str]:
        '''
        Получить параметры ресурсной записи
        '''
        pass

    @make_request
    def records_update(self, domain_id: int, record_id: int, content: str, email: str, name: str, port: int, priority: int, target: str, ttl: int, type: str, weight: int) -> Tuple[str, int, str]:
        '''
        Обновить ресурсную запись
        '''
        pass

    @make_request
    def records_list_by_domain_name(self, domain_name: str, limit: int = 1000, offset: int = 0) -> Tuple[str, int, str]:
        '''
        Получить список записей, принадлежащих заданному домену по имени
        '''
        pass

    @make_request
    def records_batch_update(self, domain_name: str, create, delete, update) -> Tuple[str, int, str]:
        '''
        Операции над несколькими записями, принадлежащими домену
        '''
        pass

    def record_id(self, domain, record_name: str, record_type: str, content: str = '') -> int:
        '''
        Возвращает id записи из домена (по имени или id) по её имени 
        В случае если найдено несколько подходящих записей или ни одной возвращает 0
        '''
        if record_type not in RECORDS_TYPE:
            return 0
        if (record_type != "SRV") and (content is None):
            return 0
        if type(domain) is int:
            domain_id=domain
            domain_name=self.domain_name(domain_id=domain_id)
        else:
            domain_id=self.domain_id(domain)
            domain_name=domain
        if record_name == '@':
            record_name = domain_name
        limit=100
        offset=0
        response, _, h = self.records_list_by_domain_id(domain_id=domain_id, limit=limit, offset=offset)
        records_total_count=int(h.get('x-total-count',0))
        if records_total_count == 0:
            return 0
        records=[]
        while True:
            records += [record for record in response if (record.get('type') == record_type) and (record.get('name') == record_name) and (record.get('content','') == content)]
            offset += limit
            if offset > records_total_count:
                break
            response, _, _ = self.records_list_by_domain_id(domain_id=domain_id, limit=limit, offset=offset)
        record_id=lambda r: int(r[0]['id']) if len(r) == 1 else 0
        return record_id(records)

    @make_request
    def ptr_list(self, limit: int = 1000, offset: int = 0) -> Tuple[str, int, str]:
        '''
        Получить список обратных записей
        '''
        pass

    @make_request
    def ptr_create(self, content: str, ip: str) -> Tuple[str, int, str]:
        '''
        Создать обратную запись
        '''
        pass

    @make_request
    def ptr_delete(self, ptr_id: int) -> Tuple[str, int, str]:
        '''
        Удалить обратную запись
        '''
        pass

    @make_request
    def ptr_get(self, ptr_id: int) -> Tuple[str, int, str]:
        '''
        Получить информацию по заданной записи
        '''
        pass

    @make_request
    def ptr_update(self, ptr_id: int, content: str, ip: str) -> Tuple[str, int, str]:
        '''
        Обновить обратную запись
        '''
        pass

    @make_request
    def tags_list(self) -> Tuple[str, int, str]:
        '''
        Получить список тэгов
        '''
        pass

    @make_request
    def tags_create(self, name: str, domains) -> Tuple[str, int, str]:
        '''
        Создать тэг
        '''
        pass

    @make_request
    def tags_delete(self, tag_id: int) -> Tuple[str, int, str]:
        '''
        Удалить тэг
        '''
        pass

    @make_request
    def tags_get(self, tag_id: int) -> Tuple[str, int, str]:
        '''
        Получить информацию о заданном тэге
        '''
        pass

    @make_request
    def tags_update(self, tag_id: int, name: str, domains) -> Tuple[str, int, str]:
        '''
        Обновить тэг
        '''
        pass
