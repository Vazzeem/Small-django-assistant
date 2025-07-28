"""
URL configuration for myassistance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from myapp import views
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('login/', views.login, name='login'),
    path('', views.home, name='home'),
    path('ui/', views.ui, name='ui'),
    path('signup/', views.signup, name='signup'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('privacy/', views.privacy_policy, name='privacy'),
     path("google7cc9fe86a6d7e7a8.html", TemplateView.as_view(template_name="google7cc9fe86a6d7e7a8.html")),
]

# urlpatterns += templates_urlpatterns = []()
    

urlpatterns += staticfiles_urlpatterns()