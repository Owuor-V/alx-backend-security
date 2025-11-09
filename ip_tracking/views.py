from django.shortcuts import render
from django.http import HttpResponse
from ratelimit.decorators import ratelimit

# Example login view
@ratelimit(key='ip', rate='10/m', method='POST', block=True)  # Authenticated users
@ratelimit(key='ip', rate='5/m', method='POST', block=True)   # Anonymous users
def login_view(request):
    if request.method == 'POST':
        # Your login logic here
        return HttpResponse("Login attempt processed.")
    return render(request, 'ip_tracking/login.html')

