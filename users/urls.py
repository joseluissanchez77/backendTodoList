from django.urls import path
from knox import views as knox_views
from . import views


urlpatterns = [
    path('login/', views.login_api),
    # path('user/', views.get_user_data),UserAPI.as_view()
    path('user/', views.UserData.as_view()),
    path('register/', views.register_api),
    path('logout/', knox_views.LogoutView.as_view()),
    path('logoutall/', knox_views.LogoutAllView.as_view()),
    path('list-user/', views.get_list_users),
]