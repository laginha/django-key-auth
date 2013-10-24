# Create your views here.
from django.http import HttpResponse
from keyauth.decorators import key_required

def view_key_not_required(request):
    return HttpResponse('success')

@key_required
def view_key_required(request):
    return HttpResponse('success')
