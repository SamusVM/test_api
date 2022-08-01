from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('my_auth.urls', namespace='my_auth')),
    path('api/', include('my_api.urls', namespace='my_api')),

]
