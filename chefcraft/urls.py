from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path
from recipe.views import (
    RecipeList, RecipeCreate, RecipeDelete, RecipeDetail, RecipeUpdate, RecipeSearch, IngredientDetail
)
from common.views import CommonLoginView, CommonLogoutView, CommonRegisterView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', CommonLoginView.as_view(), name='login'),
    path('logout/', CommonLogoutView.as_view(), name='logout'),
    path('register/', CommonRegisterView.as_view(), name='register'),
    path('share/', RecipeCreate.as_view(), name='share_recipe'),
    path('delete/<slug:slug>/', RecipeDelete.as_view(), name='delete_recipe'),
    path('edit/<slug:slug>/', RecipeUpdate.as_view(), name='update_recipe'),
    path('search/', RecipeSearch.as_view(), name='search_recipe'),
    path('ingredient/<slug:slug>/', IngredientDetail.as_view(), name='ingredient_details'),
    path('<slug:slug>/', RecipeDetail.as_view(), name='detail_recipe'),
    path('', RecipeList.as_view(), name='index'),
]


if settings.DEBUG:
    urlpatterns += [
        path(
            '{media_root}<path:path>'.format(media_root=settings.MEDIA_URL.lstrip('/')),
            serve, {'document_root': settings.MEDIA_ROOT}
        )
    ]
