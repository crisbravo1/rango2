from django.contrib import admin
from tango.models import Category,Page , UserProfile

# Register your models here.



class CategoryAdmin(admin.ModelAdmin): # hace que se llene el slug al momento
                                       # de agregar el nombre de una categoria
	prepopulated_fields ={'slug':('name',)}

class PageAdmin(admin.ModelAdmin):

	list_display=('category','title','url')

admin.site.register(Page,PageAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(UserProfile)
