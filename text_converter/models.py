class TextConverterModel:
    def __init__(self, text, voice, preset):
        self.text = text
        self.voice = voice
        self.preset = preset


class AddVoiceModel:
    def __init__(self, audio_name):
        self.audio_name = audio_name
