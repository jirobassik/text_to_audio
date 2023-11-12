from django.core.validators import FileExtensionValidator, MaxValueValidator
from django import forms
import magic

# TODO Добавить валидацию на кол-во файлов
class MultipleFileExtensionValidator(FileExtensionValidator):

    def __call__(self, value):
        if isinstance(value, (list, tuple)):
            for val in value:
                super().__call__(val)
        else:
            super().__call__(value)


class ContentValidator(FileExtensionValidator):
    message = 'Неподдерживаемый тип файла'

    def __call__(self, value):
        if isinstance(value, (list, tuple)):
            self.many_files(value)
        else:
            self.one_file(value)

    def validate_content(self, file):
        file_mime_type = magic.from_buffer(file.read(1024), mime=True)
        return file_mime_type in self.allowed_extensions

    def many_files(self, files):
        for file in files:
            self.one_file(file)

    def one_file(self, file):
        if not self.validate_content(file):
            raise forms.ValidationError(self.message)


class MaxFileSizeValidation(MaxValueValidator):
    message = 'Размер файла должен быть не более 2 мб'

    def __call__(self, value):
        if isinstance(value, (list, tuple)):
            for val in value:
                super().__call__(val)
        else:
            super().__call__(value)

    def clean(self, x):
        return x.size


extension_validation = MultipleFileExtensionValidator(('wav',))
content_validation = ContentValidator(('audio/wav', 'audio/x-wav',))
max_size_validation = MaxFileSizeValidation(2097152)
