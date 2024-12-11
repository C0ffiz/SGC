from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.http import HttpResponseForbidden

class SubdomainMiddleware(MiddlewareMixin):
    def process_request(self, request):
        host = request.get_host().split('.')
        if len(host) > 2:
            # Extract subdomain: 'riviera' from 'riviera.sgc.com'
            subdomain = host[0]
        else:
            subdomain = None
        
        request.subdomain = subdomain

class CondominiumAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Call the next middleware or view
        response = self.get_response(request)

        # Only check access for authenticated users
        if request.user.is_authenticated:
            # Example of fetching a requested condominium (via URL parameters)
            requested_condominio = request.GET.get('condominio', None)

            # Ensure requested_condominio is valid and matches the user's assigned condominium
            if requested_condominio:
                try:
                    # Check if the requested condominium matches the user's condominium
                    if int(requested_condominio) != request.user.n_condominio.n_condominio:
                        return redirect('exibirLogin')  # Redirect to the login page
                except (ValueError, TypeError):
                    # Handle invalid integer conversion or None case
                    return redirect('exibirLogin')  # Redirect to the login page

        return response

