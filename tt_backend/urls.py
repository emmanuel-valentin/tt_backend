from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('djangoapp.urls.urls_auth')),
    path('api/activities/', include('djangoapp.urls.urls_activities')),
    path('api/exercises/', include('djangoapp.urls.urls_exercises')),
    path('api/users/', include('djangoapp.urls.urls_users')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)