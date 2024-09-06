from django.http import HttpResponsePermanentRedirect


class RemoveSlashMiddleware:
    """
    Middleware to remove trailing slashes from URLs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the path ends with a slash and is not the root path
        if request.path_info != '/' and request.path_info.endswith('/'):
            # Redirect to the URL without the trailing slash
            return HttpResponsePermanentRedirect(request.path_info[:-1])

        return self.get_response(request)