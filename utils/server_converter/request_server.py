import ssl

import requests


class Request:
    def __init__(self, model_name: str):
        self.__model_name = model_name
        self.__server_name = 'http://192.168.43.99:8000/api/v1/'

    @classmethod
    def converter_model(cls):
        return cls('converter')

    @classmethod
    def user_model(cls):
        return cls('user-vote')

    @classmethod
    def admin_model(cls):
        return cls('admin-vote')

    def get_request(self, data):
        return requests.get(f'{self.server_name + self.model_name}/', data=data,
                            headers={'Content-Type': 'application/json'},
                            verify=ssl.CERT_NONE) # Попробовать {'Connection':'Keep-Alive'}

    def post_request_data(self, data):
        return requests.post(f'{self.server_name + self.model_name}/',
                             files=data, )

    def delete_request_data(self, data):
        return requests.delete(f'{self.server_name + self.model_name}/', data=data,
                               headers={'Content-Type': 'application/json'})

    @property
    def model_name(self):
        return self.__model_name

    @property
    def server_name(self):
        return self.__server_name
