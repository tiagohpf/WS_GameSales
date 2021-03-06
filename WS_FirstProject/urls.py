"""WS_FirstProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import app
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', app.views.file_status, name='index'),
    path('all_tuples', app.views.list_all_tuples, name='all_tuples'),
    path('games_list', app.views.check_games_list, name='games_list'),
    path('games_platform', app.views.check_games_platform, name='games_platform'),
    path('new_game', app.views.add_new_game_record, name='new_game'),
    path('remove_game', app.views.remove_game, name='remove_game'),
    path('console_inference', app.views.add_console_inference, name='console_inference'),
    path('region_inference', app.views.add_region_inference, name='region_inference'),
    path('release_inference', app.views.add_release_inference, name='release_inference')
]
