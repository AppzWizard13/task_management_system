from django.shortcuts import render
from django.views import View


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
        """
        Render the custom 404 error page.

        Args:
            request (HttpRequest): The incoming request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponse: Rendered 404 page response.
        """
        context = {
            'title': 'Page Not Found',
            'message': 'Oops! The page you are looking for does not exist.',
        }
        return render(request, self.template_name, context, status=404)
