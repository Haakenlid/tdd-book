import sys
from django.contrib.auth import authenticate, login
# from django.shortcuts import redirect
from django.http import HttpResponse

def persona_login(request):
    user = authenticate(assertion=request.POST.get('assertion'))
    if user:
        login(request, user)
    return HttpResponse('OK')

# def login(request):
#     print('login view', file=sys.stderr)
#     assertion = request.POST['assertion']
#     # user = PersonaAuthenticationBackend().authenticate(assertion)
#     user = authenticate(assertion=assertion)
#     if user is not None:
#         auth_login(request, user)
#     return redirect('/')

# def logout(request):
#     auth_logout(request)
#     return redirect('/')