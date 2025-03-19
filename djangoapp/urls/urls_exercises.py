from django.urls import path
from djangoapp.views import ExercisesView

urlpatterns = [
    path('', ExercisesView.getExercises, name='getExercises'),
]