from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djangoapp.urls.urls_auth')),
    path('api/activities/', include('djangoapp.urls.urls_activities')),
    path('api/exercises/', include('djangoapp.urls.urls_exercises')),

    path('api/users/', include('djangoapp.urls.urls_users')),
]