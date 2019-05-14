from django.db import models
from django.db.models import Avg
from django.utils.text import slugify
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

    @property
    def published_recipes(self):
        return self.recipes.filter(is_published=True)

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
    slug = models.SlugField(max_length=50, unique=True)
    image = models.ImageField(upload_to=recipes_directory_path)
    description = models.TextField()
    difficulty = models.IntegerField(choices=DIFFICULTY_CHOICES, default=EASY)
    ingredients = models.ManyToManyField(Ingredient, related_name='recipes')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='recipes')
    is_published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super(Recipe, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def likes_count(self) -> int:
        return self.likes.count()

    @property
    def average_rate(self) -> float:
        rate = self.rates.aggregate(avg_rate=Avg('point'))['avg_rate']
        if not rate:
            return 0
        return rate

    @property
    def vote_count(self) -> int:
        return self.rates.count()

    @property
    def author_name(self) -> str:
        name = self.author.get_full_name()
        if name:
            return name
        return self.author.username

    class Meta:
        ordering = ('-created_at',)


class Like(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='liked_recipes')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

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
        return str(self.pk)

    class Meta:
        ordering = ('user', '-created_at')
