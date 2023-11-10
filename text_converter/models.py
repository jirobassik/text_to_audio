class TextConverterModel:
    def __init__(self, text, voice, preset, owner):
        self.text = text
        self.voice = voice
        self.preset = preset
        self.owner = owner


class AddVoiceModel:
    def __init__(self, audio_name, creator):
        self.audio_name = audio_name
        self.creator = creator
