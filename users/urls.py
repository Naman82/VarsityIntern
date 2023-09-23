from django.urls import path,re_path,include
from . import views

urlpatterns=[
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path('user-signup', views.UserView.as_view(), name='user-signup'),
    path('user-login', views.TokenViewNew.as_view(), name='token'),
    path('user-convert-token', views.convertTokenViewNew.as_view(), name='convert-token'),

    # profile-routes
    path('user-profile/',views.ProfileView.as_view(),name='user-profile'),
]