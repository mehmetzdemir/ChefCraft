from django.contrib import admin
from recipe.models import Recipe, Ingredient, Like, Rate


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "difficulty", "author", "is_published", "view_count", "created_at")
    list_filter = ("difficulty", "is_published", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug", "recipe_count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    pass
