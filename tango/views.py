from django.shortcuts import render
from django.http import HttpResponse
import os
def index(request):
	context_dict={'boldmessage':"I am bold font from the context"}
	return render(request,'tango/index.html',context_dict)
# Create your views here.

def about(request):
	context_dict={'boldmessage':"Mi nombre es coronel blanco"}
	return render(request,'tango/about.html',context_dict)
	##return HttpResponse("Hola")#"Hi : Aqui retornas <a href='/tango'>tango</a>")##

def prueba(request):
	return HttpResponse(os.path.dirname(__file__))

