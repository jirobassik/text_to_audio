from rest_framework import serializers


class TextConverterSerializer(serializers.Serializer):
    text = serializers.CharField()
    voice = serializers.CharField()
    preset = serializers.CharField()
    owner = serializers.CharField()


class AddVoiceSerializer(serializers.Serializer):
    audio_name = serializers.CharField()
    creator = serializers.CharField()
