from django.urls import path
from .views import *

urlpatterns = [
    path("", SessionList.as_view(), name="session_list"),
    path("details/<int:pk>/", SessionDetails.as_view(), name="session_detail"),
    path("create/", SessionCreate.as_view(), name="session_create"),
    path("<int:pk>/edit/", SessionUpdate.as_view(), name="session_edit"),  # Make sure this line exists
    path("<int:pk>/delete/", SessionDelete.as_view(), name="session_delete"),
]