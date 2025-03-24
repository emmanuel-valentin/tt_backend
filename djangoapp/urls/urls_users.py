from django.urls import path
from djangoapp.views.user import PhysiotherapistView, PatientView

urlpatterns = [
    path('physiotherapist/<int:id>', PhysiotherapistView.getPhysiotherapistById, name='getPhysiotherapistById'),
    path('physiotherapist/update', PhysiotherapistView.updatePhysiotherapist, name='updatePhysiotherapistById'),
    path('patient/<int:id>', PatientView.getPatientById, name='getPatientById'),
    path('patient/update', PatientView.updatePatient, name='updatePhysiotherapistById'),
]