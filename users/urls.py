from django.urls import path
from .views import *

urlpatterns = [
    path('create_user_api', UserView.as_view({'post': 'create_user_api'}), name='create_user_api'),
    # path('login_user_api', UserLoginView.as_view({'post': 'login_user_api'}), name='login_user_api'),
    path('login_user_api', UserLoginView.as_view(), name="user-login"),
]
