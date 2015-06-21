from django.shortcuts import render
from django.http import HttpResponse , HttpResponseRedirect
import os
from tango.models import Category, Page
from tango.forms import CategoryForm, PageForm, UserProfileForm ,UserForm
from django.contrib.auth import authenticate , login ,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.shortcuts import redirect


def index(request):
	category_list=Category.objects.all()
	page_list=Page.objects.order_by('-views')[:5]
	#category_list=Category.objects.order_by('-likes')[:7]
	context_dict={'categories':category_list, 'pages': page_list}
	# Get the number of visits to the site.
	# We use the COOKIES.get() function to obtain the visits cookie.
	# If the cookie exists, the value returned is casted to an integer.
	# If the cookie doesn't exist, we default to zero and cast that.

	#visits=int(request.COOKIES.get('visits','1'))
	visits=request.session.get('visits')
	if not visits:
		visits=1
	reset_last_visit_time=False

	last_visit=request.session.get('last_visit')

	if last_visit:
		last_visit_time=datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

		# If it's been more than a day since the last visit...
		if (datetime.now() - last_visit_time).days > 0:
			visits = visits + 1
			# ...and flag that the cookie last visit needs to be updated
			reset_last_visit_time = True
	else:
		# Cookie last_visit doesn't exist, so flag that it should be set.
		reset_last_visit_time = True

	if reset_last_visit_time:
		request.session['last_visit']=str(datetime.now())
		request.session['visits']=visits

	context_dict['visits']=visits

	response=render(request,'tango/index.html',context_dict)

	# Return response back to the user, updating any cookies that need changed.
	return response




	##context_dict={'boldmessage':"I am bold font from the context"}
	#return render(request,'tango/index.html',context_dict)
# Create your views here.

def about(request):
	if request.session.get('visits'):
		count=request.session.get('visits')
	else:
		count=0
	context_dict={'boldmessage':"Mi nombre es coronel blanco",'visits':count}
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
		pages=Page.objects.filter(category=category).order_by('-views')
		context_dict['pages']=pages
		context_dict['category']=category
		context_dict['category_slug']=category_name_slug

	except Category.DoesNotExist:

		pass

	return render(request,'tango/category.html',context_dict)

@login_required
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
@login_required
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

	context_dict = {'form':form, 'category': cat }

	return render(request, 'tango/add_page.html', context_dict)

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.



	registered = False

	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
		# Attempt to grab information from the raw form information.
		# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		profile_form = UserProfileForm(data=request.POST)

		# If the two forms are valid...
		if user_form.is_valid() and profile_form.is_valid():
			# Save the user's form data to the database.
			user = user_form.save()

			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

			# Now sort out the UserProfile instance.
			# Since we need to set the user attribute ourselves, we set commit=False.
			# This delays saving the model until we're ready to avoid integrity problems.
			profile = profile_form.save(commit=False)
			profile.user = user


			# Did the user provide a profile picture?
			# If so, we need to get it from the input form and put it in the UserProfile model.
			if 'picture' in request.FILES:
				profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
			profile.save()

            # Update our variable to tell the template registration was successful.
			registered = True

		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
		# They'll also be shown to the user.
		else:
			print user_form.errors, profile_form.errors

	# Not a HTTP POST, so we render our form using two ModelForm instances.
	# These forms will be blank, ready for user input.
	else:
		user_form = UserForm()
		profile_form = UserProfileForm()

    # Render the template depending on the context.
	return render(request,
			'tango/register.html',
			{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

def user_login(request):

	if request.method =='POST':  ## validacion para pedir datos o recibir

		username=request.POST.get('username')
		password=request.POST.get('password')

		user= authenticate(username=username, password=password)
		if user: ## si tengo el objeto user si estaba en la database (y la contrasena estaba bien)

			if user.is_active:

				login(request,user)
				return HttpResponseRedirect('/tango/')
			else:
				return HttpResponse('Your Tango account is disabled')
		else:
			## En este caso hubo un bad login
			print "Invalid login details: {0}, {1}".format(username,password)
			return HttpResponse("Invalid login details suplied")
	else:

		return render(request,'tango/login.html',{})

@login_required ## decorator que si esta sobre la funcion indica que debe loguearme para ver el contenido
def restricted(request):

	return render(request, 'tango/restricted.html',{})

@login_required
def user_logout(request):
	logout(request) ## sabemos que ya el usuario esta conectado

	return HttpResponseRedirect('/tango/')

def track_url(request):
	page_id=None
	url='/tango/'
	if request.method == 'GET':

		if 'page_id' in request.GET:
			page_id= request.GET['page_id']
			try:
				page=Page.objects.get(id=page_id)
				page.views=page.views +1
				page.save()
				url=page.url
			except:
				pass
	return redirect(url)























