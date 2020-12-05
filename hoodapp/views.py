
from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import SuperuserProfile,AdminProfile,Business
from .serializer import SuperuserSerializer

# Create your views here.
class SuperuserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_superuser:
            pass
        else:
            raise Http404()       
    
    def get_supervisor(self, pk):
        try:
            return SuperuserProfile.objects.get(pk=pk)
        except SuperuserProfile.DoesNotExist:
            raise Http404()

class OccupantList(APIView):
    def get(self, request, format=None):
        all_resident = OccupantListProfile.objects.all()
        serializers = OccupantSerializer(all_resident, many=True)
        return Response(serializers.data)

class BusinessList(APIView):
    def get(self, request, format=None):
        all_business = Business.objects.all()
        serializers = BusinessSerializer(all_business, many=True)
        return Response(serializers.data)
