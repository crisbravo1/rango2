from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):

	name=models.CharField(max_length=128, unique=True)
	views=models.IntegerField(default=0)
	likes=models.IntegerField(default=0)
	slug=models.SlugField(unique=True)

	def save(self, *args, **kwargs):
		self.slug=slugify(self.name)
		super(Category, self).save(*args,**kwargs)


	def __str__(self):

		return self.name

class Page(models.Model):

	category=models.ForeignKey(Category)
	title= models.CharField(max_length=128)
	url=models.URLField()
	views=models.IntegerField(default=0)

	def __str__(self):

		return self.title

class UserProfile(models.Model):
	# Linea requerida. EL perfil del usuario solo esta asociado a una instancia
	# de user
	user=models.OneToOneField(User)


	# otros atributos
	website=models.URLField(blank=True)
	picture=models.ImageField(upload_to='profile_images',blank=True)
	# upload_to es un atributo que dice donde se guardara la imagen del usuario

	def __unicode__(self):
		return self.user.username


