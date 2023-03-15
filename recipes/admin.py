from django.contrib import admin

from .models import Category, Recipe

# Register your models here.


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author', 'created_at', 'is_published',)
    list_display_links = ('id', 'title')
    search_fields = ('id', 'title', 'description', 'slug', 'preparation_steps')
    list_filter = 'category', 'author', 'is_published', 'preparation_steps_is_html'  # noqa
    list_per_page = 20
    list_editable = ('is_published',)
    ordering = ('-id',)
    # prepopulated_fields = usado para criar slug seguindo um fiel
    # de algum campo
    prepopulated_fields = {
        "slug": ('title',)
    }


class CategoryAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
