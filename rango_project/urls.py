from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from registration.backends.simple.views import RegistrationView

##Create a new class that redirects the user to the index page, if successful at logging

class MyRegistrationView(RegistrationView):

	def get_success_url(self,request,user):

		return '/tango/'


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rango_project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^tango/', include('tango.urls')), # ADD THIS NEW TUPLE!
    url(r'^accounts/register/$',MyRegistrationView.as_view(), name='registration_register'),
    (r'^accounts/',include('registration.backends.simple.urls')),
)
if settings.DEBUG:
	urlpatterns +=patterns(
	  'django.views.static',
	  (r'^media/(?P<path>.*)',
	  'serve',
	  {'document_root':settings.MEDIA_ROOT}), )
