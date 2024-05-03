"""
URL configuration for Firstproject project.

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
from django.urls import path
from library import views

urlpatterns = [
    path('',views.home,name="home"),
    path('index',views.index,name="index"),
    path('student',views.student,name="student"),
    path('books',views.books,name="books"),
    path('insert',views.insertdata,name="insertdata"),
    path('insertbook',views.insertbook,name="insertbook"),
    path('update/<id>',views.updateData,name="updateData"),
    path('delete/<id>',views.deleteData,name="deleteData"),
    path('loginstu',views.loginstu,name="loginstu"),
    path('registerstu',views.registerstu,name="registerstu"),
    path('issue',views.issue,name='issue'),
    path('return_item',views.return_item,name='return_item'),
    path('logout',views.logout,name='logout'),
    
]
