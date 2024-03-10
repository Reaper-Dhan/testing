from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not request.path.startswith(reverse('signIn')):
            # Redirect to login page if the user is not authenticated and the requested path is not the login page
            return redirect('signIn')
        return self.get_response(request)
