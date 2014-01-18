from django.shortcuts import render

def index(request):
    context = {}
    return render(request, 'cta/index.html', context)
