from django.urls import path
from djangoapp.views import ActivitiesView

urlpatterns = [
    path('assignments', ActivitiesView.getActivities, name='getActivities'),
    path('assign', ActivitiesView.asignarEjercicio, name='asignarEjercicio'),
    path('assignment/<int:id>', ActivitiesView.getActivitiesById, name='getActivitiesById'),
    path('assigned/', ActivitiesView.actualizarEjercicioAsignado, name='actualizarActivitiesById'),
    path('assigned/delete', ActivitiesView.eliminarEjercicioAsignado, name='eliminarActivitiesById'),
    path('assigned/submit', ActivitiesView.subirEjercicioAsignado, name='subirActivitiesById')
]
