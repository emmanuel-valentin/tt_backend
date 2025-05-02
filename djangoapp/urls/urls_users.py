from django.urls import path
from djangoapp.views.user import PhysiotherapistView, PatientView, UserView

urlpatterns = [
    path('physiotherapist/<int:id>', PhysiotherapistView.getPhysiotherapistById, name='getPhysiotherapistById'),
    path('physiotherapist/update', PhysiotherapistView.updatePhysiotherapist, name='updatePhysiotherapistById'),

    path('physiotherapist/links', PhysiotherapistView.getAllLinks, name='getLinks'),
    path('physiotherapist/request-links', PhysiotherapistView.getPendingLinks, name='getLinks'),
    path('physiotherapist/patients', PhysiotherapistView.getAcceptedLinks, name='getAcceptedLinks'),

    path('physiotherapist/link/accept', PhysiotherapistView.aceeptLink, name='acceptLink'),
    path('physiotherapist/link/reject', PhysiotherapistView.rejectLink, name='rejectLink'),

    path('physiotherapist/feedback', PhysiotherapistView.sendFeedback, name='sendFeedback'),


    path('patient/<int:id>', PatientView.getPatientById, name='getPatientById'),
    path('patient/update', PatientView.updatePatient, name='updatePhysiotherapistById'),
    path('patient/link', PatientView.linkPatientToPhysiotherapist, name='linkPatientToPhysiotherapist'),
    path('patient/links', PatientView.getLinks, name='getLinks'),

    path('<int:id>', UserView.getUserById, name='getUserById'),
    path('profile', UserView.getUserProfile, name='getUserProfile'),
    path('profile/update', UserView.updateUser, name='updateUserProfile')
]