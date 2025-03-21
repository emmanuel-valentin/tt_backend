from django.urls import path
from djangoapp.views.user import PhysiotherapistView, PatientView

urlpatterns = [
    path('physiotherapist/<int:id>', PhysiotherapistView.getPhysiotherapistById, name='getPhysiotherapistById'),
    path('patient/<int:id>', PatientView.getPatientById, name='getPatientById'),
]