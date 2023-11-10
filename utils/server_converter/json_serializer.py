from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from io import BytesIO

class JsonSerializer:
    def __init__(self, model, model_serializer):
        self.model = model
        self.model_serializer = model_serializer

    def encode(self, **kwargs):
        model = self.model(**kwargs)
        model_sr = self.model_serializer(model)
        return JSONRenderer().render(model_sr.data)

    def decode(self, raw_data, many=True):
        stream = BytesIO(raw_data)
        data = JSONParser().parse(stream)
        serializer = self.model_serializer(data=data, many=many)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data
