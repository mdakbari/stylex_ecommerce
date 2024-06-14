
from django.shortcuts import redirect
from django.urls import reverse

class AdminAccessMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        if request.META.get('QUERY_STRING'):
            path = path + '?' + request.META.get('QUERY_STRING')
        if '?currency=' in path:
            print('path true== ', path)
            try:
                request.session['currency'] = request.META.get('QUERY_STRING').split('=')[1]
            except:
                request.session['currency'] = request.META.get('QUERY_STRING')
    
            return redirect('{}'.format(path.split('?')[0])) 
        # Assuming you have a named URL pattern for login page
        return self.get_response(request)

        # Check if the user is logged in or not
        if not request.session.get('user'):
            # If user is not logged in, redirect to a login page or any other page
            return redirect(reverse('login'))  # Assuming you have a named URL pattern for login page
        return self.get_response(request)
        