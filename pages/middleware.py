# middleware.py

from django.shortcuts import redirect


class PageRestrictionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, user=None):
        response = self.get_response(request)
        if not request.user.is_authenticated:
            # User is not logged in, no need to check restrictions
            return response

        if not request.user.is_superuser:
            # Check if the requested page is restricted
            restricted_urls = {
                '/restricted-page',
                '/another-restricted-page',
            }

            if request.path in restricted_urls:
                allowed_groups = restricted_urls[request.path]
                if not user.groups.filter(name__in=allowed_groups).exists():
                    # User does not have access to the requested page
                    return redirect('access_denied')

        return response
