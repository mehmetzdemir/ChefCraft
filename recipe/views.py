from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.utils.text import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from recipe.models import Recipe, Ingredient
from recipe.forms import RecipeForm


class RecipeList(ListView):
    queryset = Recipe.objects.filter(is_published=True)
    template_name = 'recipe/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.annotate(
            total_recipes=Count('recipes')
        ).order_by('-total_recipes')[:6]
        return context


class RecipeCreate(LoginRequiredMixin, CreateView):
    permission_denied_message = "Please, login for adding new recipes!"
    template_name = 'recipe/add.html'
    form_class = RecipeForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        recipe = form.save(commit=False)
        recipe.author = self.request.user
        if recipe.name:
            # add unique slug
            slug = slugify(recipe.name)
            counter = 1
            while Recipe.objects.filter(slug=slug).exists():
                slug = slugify(recipe.name + ' ' + str(counter))
                counter += 1
            recipe.slug = slug
        return super(RecipeCreate, self).form_valid(form)


class RecipeDelete(DeleteView):
    model = Recipe
    template_name = 'recipe/delete.html'
    success_url = reverse_lazy('index')


class RecipeDetail(DetailView):
    model = Recipe
    template_name = 'recipe/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ingredients'] = Ingredient.objects.annotate(
            total_recipes=Count('recipes')
        ).order_by('-total_recipes')[:6]
        return context


class RecipeUpdate(UpdateView):
    form_class = RecipeForm
    model = Recipe
    template_name = 'recipe/edit.html'
    success_url = reverse_lazy('index')


class RecipeSearch(ListView):
    queryset = Recipe.objects.none()
    template_name = 'recipe/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_keywords = self.request.GET.get('q', None)
        recipes = Recipe.objects.filter(is_published=True)
        if search_keywords:
            named_recipes = recipes
            ingredient_recipes = recipes
            description_recipes = recipes
            search_keywords = search_keywords.split(',')
            for keyword in search_keywords:
                keyword = keyword.strip()
                named_recipes = named_recipes.filter(name__icontains=keyword)
                ingredient_recipes = ingredient_recipes.filter(ingredients__name__iexact=keyword)
                description_recipes = description_recipes.filter(description__icontains=keyword)
            # group by
            named_recipes = named_recipes.distinct()
            ingredient_recipes = ingredient_recipes.distinct()
            description_recipes = description_recipes.distinct()
            # exclude same data:
            if description_recipes and named_recipes:
                description_recipes = description_recipes.exclude(pk__in=named_recipes.values('pk'))
            if description_recipes and ingredient_recipes:
                description_recipes = description_recipes.exclude(pk__in=ingredient_recipes.values('pk'))
            if named_recipes and ingredient_recipes:
                named_recipes = named_recipes.exclude(pk__in=ingredient_recipes.values('pk'))
            # add data to the context
            context['named_recipes'] = named_recipes[:10]
            context['ingredient_recipes'] = ingredient_recipes[:10]
            context['description_recipes'] = description_recipes[:5]
        else:
            context['named_recipes'] = []
            context['ingredient_recipes'] = []
            context['description_recipes'] = []
        context['search_keywords'] = self.request.GET.get('q', 'Search for ingredients, names, descriptions')
        return context

