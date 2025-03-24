from django.shortcuts import render

# NOTE: api testing only subject to delete 

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Budget
from .serializers import BudgetSerializer

class HomeView(APIView):
    def get(self, request):
        return Response({"message": "Welcome!! This is temporary hompage of the app"})