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
