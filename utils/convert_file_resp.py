import cgi
from django.http import HttpResponse


def convert_to_downloable(response):
    content, content_disposition = response.content, response.headers.get('Content-Disposition')
    _, params = cgi.parse_header(content_disposition)
    filename = params.get('filename')
    response = HttpResponse(content, content_type='audio/wav')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
