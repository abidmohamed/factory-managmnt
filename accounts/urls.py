from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from . import views
from .views import LoadUserView

app_name = 'accounts'

urlpatterns = [
    path('login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),

    path('add_user/', views.add_user, name='add_user'),
    path('users_list/', views.users_list, name='users_list'),
    path('update_user/<str:pk>', views.update_user, name='update_user'),

    path('permissions_list/<str:pk>', views.permissions_list, name='permissions_list'),
    path('update_permissions/<str:pk>', views.update_permissions, name='update_permissions'),

    path('serviceworker', (TemplateView.as_view(
        template_name="serviceworker.js",
        content_type='application/javascript', )),
         name='serviceworker'),

    # API end points
    path('token/', TokenObtainPairView.as_view(), name='login_token'),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('token/verify/', TokenVerifyView.as_view()),

    path('user', LoadUserView.as_view())
]
