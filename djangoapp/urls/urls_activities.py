from django.urls import path
from djangoapp.views.activities import getActivitiesView

urlpatterns = [
    path('assigned/<int:id>', getActivitiesView.getActivitiesById, name='getActivitiesById'),
]
