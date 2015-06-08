from django.shortcuts import render
from django.http import HttpResponse
import os
from tango.models import Category, Page
from tango.forms import CategoryForm, PageForm


def index(request):

	category_list=Category.objects.order_by('-likes')[:5]
	context_dict={'categories':category_list}
	##context_dict={'boldmessage':"I am bold font from the context"}
	return render(request,'tango/index.html',context_dict)
# Create your views here.

def about(request):
	context_dict={'boldmessage':"Mi nombre es coronel blanco"}
	return render(request,'tango/about.html',context_dict)
	##return HttpResponse("Hola")#"Hi : Aqui retornas <a href='/tango'>tango</a>")##

def prueba(request):
	return HttpResponse(os.path.dirname(__file__))

def category(request,category_name_slug):
	context_dict={}

	try:
		category = Category.objects.get(slug=category_name_slug)
		context_dict['category_name']=category.name

		#Adds our results list to the template context under name pages
		pages=Page.objects.filter(category=category)
		context_dict['pages']=pages
		context_dict['category']=category
		context_dict['category_slug']=category_name_slug

	except Category.DoesNotExist:

		pass

	return render(request,'tango/category.html',context_dict)

def add_category(request):

	if request.method =='POST':
		form=CategoryForm(request.POST)

		if form.is_valid():
			form.save(commit=True)

			## Llamamo a la index view
			return index(request)
		else:

			print form.errors
	else:
		## Si no es un post request muestra la form
		form=CategoryForm()

	return render(request,'tango/add_category.html',{'form':form})

def add_page(request,category_name_slug):

	try:
		cat = Category.objects.get(slug=category_name_slug)
	except Category.DoesNotExist:
			cat = None

	if request.method == 'POST':
 		form = PageForm(request.POST)
		if form.is_valid():
			if cat:
				page = form.save(commit=False)
				page.category = cat
				page.views = 0
				page.save()
                # probably better to use a redirect here.
				return category(request, category_name_slug)
		else:
			print form.errors
	else:
		form = PageForm()

	context_dict = {'form':form, 'category': cat , 'category_name_slug':category_name_slug}

	return render(request, 'tango/add_page.html', context_dict)








