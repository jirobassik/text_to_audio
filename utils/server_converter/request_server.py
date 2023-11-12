import requests


class Request:
    def __init__(self, model_name: str):
        self.__model_name = model_name
        self.__server_name = 'https://2cc7-46-56-227-112.ngrok-free.app/api/v1/'

    @classmethod
    def converter_model(cls):
        return cls('converter')

    def get_request(self, data):
        return requests.get(f'{self.server_name + self.model_name}/', data=data,
                            headers={'Content-Type': 'application/json'})

    def post_request_data(self, data):
        return requests.post(f'{self.server_name + self.model_name}/',
                             files=data, ).content

    def delete_request_data(self, data):
        requests.delete(f'{self.server_name + self.model_name}/', data=data,
                        headers={'Content-Type': 'application/json'})

    @property
    def model_name(self):
        return self.__model_name

    @property
    def server_name(self):
        return self.__server_name
