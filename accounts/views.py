import sys
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.shortcuts import redirect

def login(request):
    print('login view', file=sys.stderr)
    assertion = request.POST['assertion']
    # user = PersonaAuthenticationBackend().authenticate(assertion)
    user = authenticate(assertion)
    if user is not None:
        auth_login(request, user)
    return redirect('/')
