from django.contrib import admin
from .models import *

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'slug']
    prepopulated_fields = {'slug':('name',)}

class BoardAdmin(admin.ModelAdmin):
    list_display = ['post_name','post_context', 'post_author', 'category','created_date', 'updated_date']
    list_filter = ['created_date', 'updated_date', 'category']

class EditAdmin(admin.ModelAdmin):
    list_display = ['board','edit_date']

admin.site.register(EditLog, EditAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Board, BoardAdmin)
