from django.contrib import admin
from .models import *

class FilesAdmin(admin.ModelAdmin):
    list_display = ['id','file','file_category','post']

class CateAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'slug']
    prepopulated_fields = {'slug':('name',)}

class ErrorLogAdmin(admin.ModelAdmin):
    list_display = ['id','title']

admin.site.register(Integrated_Files, FilesAdmin)
admin.site.register(File_Category, CateAdmin)
admin.site.register(ErrorLog, ErrorLogAdmin)