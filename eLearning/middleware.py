from django.conf import settings
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin


class RemoveSlashMiddleware:
    """
    Middleware to remove trailing slashes from URLs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip URL paths that start with '/admin' or are the root path
        if request.path_info.startswith('/admin') or request.path_info == '/':
            return self.get_response(request)

        # Check if the path ends with a slash and is not the root path
        if request.path_info != '/' and request.path_info.endswith('/'):
            # Redirect to the URL without the trailing slash
            return HttpResponsePermanentRedirect(request.path_info[:-1])

        return self.get_response(request)


class XFrameOptionsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if the request is for the media files (e.g., PDFs)
        if request.path.startswith('/media/'):
            response['X-Frame-Options'] = 'ALLOWALL'
        else:
            # Keep default behavior for other pages
            response['X-Frame-Options'] = getattr(settings, 'X_FRAME_OPTIONS', 'DENY')
        return response