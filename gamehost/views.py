from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# Just to test how the views worked again.
def index(request):
    return HttpResponse("Hello! This is the index view of gamehost.")
