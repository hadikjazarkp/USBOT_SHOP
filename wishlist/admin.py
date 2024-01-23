from django.contrib import admin
from .models import *
from django.contrib.auth.models import Group

# Register your models here.
# class WishlistAdmin(admin.ModelAdmin):
#     list_display = ('id',)
    

# admin.site.register(WishlistModel, WishlistAdmin)    

class CustomGroupAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False
    
    
admin.site.unregister(Group)
admin.site.register(Group,CustomGroupAdmin)    