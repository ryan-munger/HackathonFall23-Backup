"""
URL configuration for Bot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import authentication.views as auth_views
import help.views as help_views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='base.html'), name="index"),
    path('register/', auth_views.register, name='register'),
    path('login/', auth_views.login, name='login'),
    path('admin/', admin.site.urls),

    # bot help
    path('ask_question/', help_views.ask_question, name="ask_question"),
    path('question_history/', help_views.question_history, name="question_history"),
    # partials
    path('get_question_area/', help_views.get_question_area, name="get_question_area"),
    path('answer_question/', help_views.answer_question, name="answer_question"),
]
