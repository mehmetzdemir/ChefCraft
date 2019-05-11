from django.db import models
from django.contrib.auth import get_user_model


def recipes_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'recipes/{0}/{1}'.format(instance.author.id, filename)


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.name

    @property
    def recipe_count(self):
        return self.recipes.filter(is_published=True).count()

    class Meta:
        ordering = ('name',)


class Recipe(models.Model):
    EASY = 1
    MEDIUM = 2
    HARD = 3
    DIFFICULTY_CHOICES = (
        (EASY, 'Easy'),
        (MEDIUM, 'Medium'),
        (HARD, 'Hard'),
    )

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=50)
    image = models.ImageField(upload_to=recipes_directory_path)
    description = models.TextField()
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=EASY)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recipes')
    is_published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='liked_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pk

    class Meta:
        ordering = ('user', '-created_at')


class Rate(models.Model):
    POINT_CHOICES = (
        (0, 'Vomiting'),
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Medium'),
        (4, 'Good'),
        (5, 'Excellent')
    )
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='rated_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='rates')
    point = models.IntegerField(choices=POINT_CHOICES, default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pk

    class Meta:
        ordering = ('user', '-created_at')
