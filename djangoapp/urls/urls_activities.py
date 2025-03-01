from django.urls import path
from djangoapp.views import ActivitiesView

urlpatterns = [
    path('assignments', ActivitiesView.getActivities, name='getActivities'),
    path('assign', ActivitiesView.asignarEjercicio, name='asignarEjercicio'),
    path('assignments/<int:id>', ActivitiesView.getActivitiesById, name='getActivitiesById'),
]
