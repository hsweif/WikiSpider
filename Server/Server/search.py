
from django.http import HttpResponse
from django.shortcuts import render_to_response
def search_form(request):
    return render_to_response('search_form.html')

def search(request):  
    request.encoding='utf-8'
    if 'q' in request.GET:
        message = 'Your reseach content is:' + request.GET['q']
    else:
        message = 'You submitted a blank form'
    return HttpResponse(message)
