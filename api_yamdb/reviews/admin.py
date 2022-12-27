from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ImportMixin

from .models import Title, Genre, Category
from import_export import resources


class CategoryResources(resources.ModelResource):
    class Meta:
        model = Category


class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResources]


admin.site.register(Title)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre)
