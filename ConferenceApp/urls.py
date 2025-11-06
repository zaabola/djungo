from django.urls import path
from .views import *

urlpatterns = [
    path("liste/", ConferenceList.as_view(), name="conference_liste"),
    path("details/<int:pk>/", ConferenceDetails.as_view(), name="conference_detail"),
    path("form/", ConferenceCreate.as_view(), name="conference_add"),
    path("<int:pk>/edit/", ConferenceUpdate.as_view(), name="conference_edit"),
    path("<int:pk>/delete/", ConferenceDelete.as_view(), name="conference_delete"),
    path("submissions/", SubmissionList.as_view(), name="submission_list"),
    path("submissions/details/<str:pk>/", SubmissionDetails.as_view(), name="submission_detail"),
    path("submissions/create/", SubmissionCreate.as_view(), name="submission_create"),
    path("submissions/<str:pk>/edit/", SubmissionUpdate.as_view(), name="submission_edit"),
    path("submissions/<str:pk>/delete/", SubmissionDelete.as_view(), name="submission_delete"),
]
