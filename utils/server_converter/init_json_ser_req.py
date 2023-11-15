from text_converter.serializers import TextConverterSerializer, AddVoiceSerializer
from text_converter.models import TextConverterModel, AddVoiceModel

from utils.server_converter.request_server import Request
from utils.server_converter.json_serializer import JsonSerializer

text_converter_serializer = JsonSerializer(TextConverterModel, TextConverterSerializer)
text_converter_request = Request.converter_model()

add_delete_voice_serializer = JsonSerializer(AddVoiceModel, AddVoiceSerializer)

add_delete_voice_request_user = Request.user_model()
add_delete_voice_request_admin = Request.admin_model()
