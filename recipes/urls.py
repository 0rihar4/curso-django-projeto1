from django.urls import path

from recipes import views

app_name = 'recipes'

urlpatterns = [
    # Quanto mais especifico for uma url ex = recipes/search/, mais ao topo
    # ela deve ficar e quanto menos especifico, possuir parametros
    # variaveis, mais abaixo ela deve ficar
    path('', views.RecipeListViewHome.as_view(), name="home"),
    path('recipes/search/',
         views.RecipeListViewSearch.as_view(), name="search"),
    path('recipes/<int:pk>/', views.RecipeDetail.as_view(), name="recipe"),
    path('recipes/category/<int:category_id>/',
         views.RecipeListViewCategory.as_view(), name="category"),

]
