from django.shortcuts import render
from django.views import View
from django.conf import settings
from django.http import HttpResponse, Http404
from django.views.static import serve as django_serve
import os
class Custom404View(View):
    """
    Handle custom 404 (Page Not Found) errors.

    This view renders a user-friendly 404 error page with an
    optional context message. You can extend this to include
    custom logic like logging missing URLs, suggesting links,
    or tracking user navigation errors.
    """

    template_name = '404.html'

    def get(self, request, *args, **kwargs):

        context = {
            'title': 'Page Not Found',
            'message': 'Oops! The page you are looking for does not exist.',
        }
        return render(request, self.template_name, context, status=404)

def serve_media(request, path):
    """Serve media files in production."""
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):
        return django_serve(request, path, document_root=settings.MEDIA_ROOT)
    raise Http404("Media file not found")