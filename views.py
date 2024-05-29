# data_app/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Account, Destination
from .serializers import AccountSerializer, DestinationSerializer
from django.shortcuts import get_object_or_404
import requests


class AccountListCreateView(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class DestinationListCreateView(generics.ListCreateAPIView):
    serializer_class = DestinationSerializer

    def get_queryset(self):
        account_id = self.kwargs["account_id"]
        return Destination.objects.filter(account_id=account_id)

    def perform_create(self, serializer):
        account_id = self.kwargs["account_id"]
        account = get_object_or_404(Account, id=account_id)
        serializer.save(account=account)


class DestinationRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer


class DestinationListByAccountView(generics.ListAPIView):
    serializer_class = DestinationSerializer

    def get_queryset(self):
        account_id = self.kwargs["account_id"]
        return Destination.objects.filter(account_id=account_id)


class IncomingDataView(APIView):
    def post(self, request, *args, **kwargs):
        app_secret_token = request.headers.get("CL-X-TOKEN")
        if not app_secret_token:
            return Response(
                {"detail": "Un Authenticate"}, status=status.HTTP_401_UNAUTHORIZED
            )

        account = get_object_or_404(Account, app_secret_token=app_secret_token)
        destinations = Destination.objects.filter(account=account)

        for destination in destinations:
            headers = {
                header.split(":")[0]: header.split(":")[1].strip()
                for header in destination.headers.split(",")
            }
            if destination.http_method.lower() == "get":
                response = requests.get(
                    destination.url, params=request.data, headers=headers
                )
            elif destination.http_method.lower() == "post":
                response = requests.post(
                    destination.url, json=request.data, headers=headers
                )
            elif destination.http_method.lower() == "put":
                response = requests.put(
                    destination.url, json=request.data, headers=headers
                )
            # Handle response if needed

        return Response(
            {"detail": "Data pushed successfully"}, status=status.HTTP_200_OK
        )
