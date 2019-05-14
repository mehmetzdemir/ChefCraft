from django.contrib import admin
from django.conf import settings
from django.views.static import serve
from django.urls import path
from recipe.views import RecipeList, RecipeCreate, RecipeDelete, RecipeDetail, RecipeUpdate, RecipeSearch


urlpatterns = [
    path('admin/', admin.site.urls),
    path('share/', RecipeCreate.as_view(), name='share_recipe'),
    path('delete/<slug:slug>/', RecipeDelete.as_view(), name='delete_recipe'),
    path('edit/<slug:slug>/', RecipeUpdate.as_view(), name='update_recipe'),
    path('search/', RecipeSearch.as_view(), name='search_recipe'),
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
