from django.urls import path
from . import views
urlpatterns = [
    path('create/', views.createUser, name='createUser'),
    path('all/', views.getUsers, name='getUsers'),
    path('update/<int:userId>/', views.updateUser, name='updateUser'),
    path('delete/<int:userId>/', views.deleteUser, name='deleteUser'),
    path('login/',views.loginUser,name="loginUser"),
    path('logout/',views.logoutUser,name="logoutUser")
]