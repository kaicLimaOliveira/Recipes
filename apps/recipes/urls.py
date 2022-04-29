from django.urls import path

from apps.recipes import views

# recipes:recipe
app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListViewHome.as_view(), name="home"),
    path('receitas/buscar/', views.RecipeListViewSearch.as_view(), name="search"),
    path(
        'receitas/categoria/<int:category_id>/', 
        views.RecipeListViewCategory.as_view(), 
        name="category"
    ),
    path('receitas/<int:pk>/', views.RecipeDetail.as_view(), name="recipe"),
    path('receitas/api/v1/', views.RecipeListViewHomeApi.as_view(), name="recipe_api"),
    path('receitas/api/v1/<int:pk>/', views.RecipeDetailApi.as_view(), name="recipe_detail_api"),
    path('receitas/teoria/', views.theory, name="theory"),
]
