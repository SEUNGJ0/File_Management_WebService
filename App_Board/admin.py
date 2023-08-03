from django.contrib import admin
from .models import *



class PhotoInline(admin.TabularInline):
    model = Photo

class FileInline(admin.TabularInline):
    model = Files

class BoardAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, FileInline]
    list_display = ['post_name', 'post_author', 'category','created_date', 'updated_date']
    list_filter = ['created_date', 'updated_date', 'category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'slug']
    prepopulated_fields = {'slug':('name',)}

class EditAdmin(admin.ModelAdmin):
    list_display = ['post','edit_date']

admin.site.register(EditLog, EditAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Board, BoardAdmin)
