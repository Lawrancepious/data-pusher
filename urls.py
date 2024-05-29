# data_pusher/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("data_app.urls")),  # Include URLs from your Django app
]
# data_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # CRUD operations for Account
    path(
        "accounts/", views.AccountListCreateView.as_view(), name="account-list-create"
    ),
    path(
        "accounts/<int:pk>/",
        views.AccountRetrieveUpdateDestroyView.as_view(),
        name="account-detail",
    ),
    # CRUD operations for Destination
    path(
        "accounts/<int:account_id>/destinations/",
        views.DestinationListCreateView.as_view(),
        name="destination-list-create",
    ),
    path(
        "destinations/<int:pk>/",
        views.DestinationRetrieveUpdateDestroyView.as_view(),
        name="destination-detail",
    ),
    # Get destinations by account ID
    path(
        "accounts/<int:account_id>/destinations/",
        views.DestinationListByAccountView.as_view(),
        name="destination-list-by-account",
    ),
    # API for receiving data
    path(
        "server/incoming_data/", views.IncomingDataView.as_view(), name="incoming-data"
    ),
]
