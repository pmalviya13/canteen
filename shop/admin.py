from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Profile)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','slug']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Category,CategoryAdmin)

#product admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock','available', 'created', 'updated']
    list_filter = ['available','created','updated']
    list_editable = ['price','stock','available']
    prepopulated_fields = {'slug':('name',)}
admin.site.register(Product,ProductAdmin)

#slider admin
class SlideAdmin(admin.ModelAdmin):
    list_display = ['image_name','slide','created']
    list_filter = ['slide','created']
    prepopulated_fields = {'slug':('image_name',)}
    search_fields = ['name']
    list_editable = ['slide']
admin.site.register(Slide,SlideAdmin)