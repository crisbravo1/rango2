"""
Django settings for rango_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hp@s6n-ma9o!kw4hd=$=tk7aq$j411m00@_3o#y*g9d%$a_2b9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

## Templates for my project
TEMPLATE_PATH=os.path.join(BASE_DIR,'templates')
TEMPLATE_DIRS = (
    ## usar path absolutos y no relativos
    TEMPLATE_PATH,

)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tango',
    'registration',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'rango_project.urls'

WSGI_APPLICATION = 'rango_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATIC_PATH =os.path.join(BASE_DIR,'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (


    STATIC_PATH,


)

MEDIA_URL = '/media/' ## donde seran accesibles todos los archivos en el development server
MEDIA_ROOT = os.path.join(BASE_DIR,'media') ##donde se guardara los archivos subidos por el usuario en el disco local
#LOGIN_URL = 'tango/login/' ## me permite redirigir un usuario no log in a la pagina deseada
## en este caso la pagina de login

## Opciones para el paquete registration

REGISTRATION_OPEN=True  ## Si es true los usuarios pueden registrarse
ACCOUNT_ACTIVATION_DAYS=7 ## one week activation window
REGISTRATION_AUTO_LOGIN=True  ## si es cierto los usuarios automaticamente log-in
LOGIN_REDIRECT_URL='/tango' ## pagina que los usuario logueados llegaran
LOGIN_URL='/accounts/login' ## paginas que van los usuarios si no estan logueados
