import os
import urllib2

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponse

from django.contrib.staticfiles.views import serve as staticfiles_serve


def serve(request, path, document_root=None, insecure=False, **kwargs):
    """
    Proxies static request to middleman
    """
    if not settings.DEBUG and not insecure:
        raise ImproperlyConfigured("The staticfiles view can only be used in "
                                   "debug mode or if the the --insecure "
                                   "option of 'runserver' is used")
    url = os.path.join(settings.MIDDLEMAN_URL, path)
    try:
        response = urllib2.urlopen(url)
    except urllib2.HTTPError, exc:
        if not exc.code == 404:
            raise
        return staticfiles_serve(request, path, document_root=document_root, insecure=insecure, **kwargs)

    return HttpResponse(response.read(), status=response.code, mimetype=response.headers['content-type'])
