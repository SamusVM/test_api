from django.urls import path

from .views import SignUpAPIView, LoginAPIView, UserRetrieveUpdateAPIView, UserActivityRetrieveAPIView

app_name = 'my_auth'
urlpatterns = [
    path('me', UserRetrieveUpdateAPIView.as_view(), name='me'),
    path('activity', UserActivityRetrieveAPIView.as_view(), name='activity'),
    path('signup', SignUpAPIView.as_view(), name='signup'),
    path('login', LoginAPIView.as_view(), name='login'),

]