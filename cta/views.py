from django.shortcuts import render
import mongoengine

# ...

def index(request):
    context = {}
    return render(request, 'cta/index.html', context)

user = authenticate(username=username, password=password)
assert isinstance(user, mongoengine.django.auth.User)