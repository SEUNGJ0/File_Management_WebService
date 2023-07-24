from django.contrib import admin
from .models import *

class FilesAdmin(admin.ModelAdmin):
    list_display = ['id','file','s_category','board']

class CateAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'slug']
    prepopulated_fields = {'slug':('name',)}

class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ['id','title']

admin.site.register(Files, FilesAdmin)
admin.site.register(S_Category, CateAdmin)
admin.site.register(ErrorLog, ErrorLogAdmin)