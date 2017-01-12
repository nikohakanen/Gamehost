from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


# Just to test how the views worked again.
def homeview(request):
    return render(request, 'base.html')
