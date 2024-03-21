"""
URL configuration for finalProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.views.generic import TemplateView

from bettingApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.HomePage.as_view(), name="home"),
    path("addteam/", views.AddTeamView.as_view(), name="addteam"),
    path("addleague/", views.AddLeagueView.as_view(), name="addleague"),
    path("addcountry/", views.AddCountryView.as_view(), name="addcountry"),
    path("addgame/", views.AddGameView.as_view(), name="addgame"),
    path("teamlist/", views.TeamListView.as_view(), name="teamlist"),
    path("editteam/<int:pk>", views.EditTeamView.as_view(), name="editteam"),
    path("deleteteam/<int:pk>", views.DeleteTeamView.as_view(), name="deleteteam"),
    path("leaguelist/", views.LeagueListView.as_view(), name="leaguelist"),
    path("editleague/<int:pk>", views.EditLeagueView.as_view(), name="editleague"),
    path("deleteleague/<int:pk>", views.DeleteLeagueView.as_view(), name="deleteleague"),
    path("editcountry/<int:pk>", views.EditCountryView.as_view(), name="editcountry"),
    path("createuser/", views.CreateUserView.as_view(), name="createuser"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("userview/", views.UserView.as_view(), name="userview"),
    path("addscore/", views.AddScoreToGameView.as_view(), name="addscore"),
]
