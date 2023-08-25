from django.contrib import admin
from .models import *

class AdminViewNews(admin.ModelAdmin):
    list_display = ['title', 'id', 'date_create']
    filter_horizontal = ['categories']

class AdminViewOrders(admin.ModelAdmin):
    list_display = ['user', 'id', 'date_create', 'date_update', 'get_total_cost']
    filter_horizontal = ['services']

class AdminViewServices(admin.ModelAdmin):
    list_display = ['title', 'id', 'date_create', 'price']
    filter_horizontal = ['categories']

admin.site.register(User)
admin.site.register(News, AdminViewNews)
admin.site.register(Services, AdminViewServices)
admin.site.register(CategoriesNews)
admin.site.register(CategoriesServices)
admin.site.register(NewsComments)
admin.site.register(Orders, AdminViewOrders)