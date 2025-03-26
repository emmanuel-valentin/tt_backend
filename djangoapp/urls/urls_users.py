from django.urls import path
from djangoapp.views.user import PhysiotherapistView, PatientView

urlpatterns = [
    path('physiotherapist/<int:id>', PhysiotherapistView.getPhysiotherapistById, name='getPhysiotherapistById'),
    path('physiotherapist/update', PhysiotherapistView.updatePhysiotherapist, name='updatePhysiotherapistById'),
    path('physiotherapist/links', PhysiotherapistView.getLinks, name='getLinks'),
    path('physiotherapist/feedback', PhysiotherapistView.sendFeedback, name='sendFeedback'),


    path('patient/<int:id>', PatientView.getPatientById, name='getPatientById'),
    path('patient/update', PatientView.updatePatient, name='updatePhysiotherapistById'),
    path('patient/link', PatientView.linkPatientToPhysiotherapist, name='linkPatientToPhysiotherapist'),
    path('patient/links', PatientView.getLinks, name='getLinks'),
]