
from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import SuperuserProfile,AdminProfile,Business,Neighborhood
from .serializer import *
from django.conf import settings

# Create your views here.


#Superuser apis
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

    
    def get(self, request, pk, format=None):
        print(request.user)
        self.check_role(request)
        this_superuser = self.get_superuser(pk)
        serializers = SuperuserSerializer(this_superuser)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        self.check_role(request)
        this_superuser = self.get_supervisor(pk)
        serializers = SuperuserSerializer(this_superuser, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.check_role(request)
        this_superuser = self.get_superuser(pk)
        this_superuser.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#Admin API
class AdminProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_superuser or request.user.is_admin:
            pass
        else:
            raise Http404()       
    
    def get_admin(self, pk):
        try:
            return AdminProfile.objects.get(pk=pk)
        except AdminProfile.DoesNotExist:
            raise Http404()    

    def get(self, request, pk, format=None):
        self.check_role(request)
        this_admin = self.get_admin(pk)
        serializers = AdminSerializer(this_admin)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        self.check_role(request)
        this_admin = self.get_admin(pk)
        serializers = AdminSerializer(this_admin, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        self.check_role(request)
        this_admin = self.get_admin(pk)
        this_admin.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminsView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_superuser:
            pass
        else:
            raise Http404()    

    def get(self, request, format=None):
        self.check_role(request)
        all_admins = AdminProfile.objects.all()
        serializers = AdminSerializer(all_admins, many=True)
        return Response(serializers.data) 


#occupants API View
class OccupantProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_superuser or request.user.is_admin or request.user.is_occupant:
            pass
        else:
            raise Http404()       
    
    def get_occupant(self, pk):
        try:
            return OccupantProfile.objects.get(pk=pk)
        except OccupantProfile.DoesNotExist:
            raise Http404()    

    def get(self, request, pk, format=None):
        self.check_role(request)
        this_occupant = self.get_occupant(pk)
        serializers = OccupantSerializer(this_occupant)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        self.check_role(request)
        this_occupant = self.get_occupant(pk)
        serializers = OccupantSerializer(this_occupant, request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        self.check_role(request)
        this_occupant = self.get_occupant(pk)
        this_occupant.user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#all occupants view

class OccupantsView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_superuser or request.user.is_admin:
            pass
        else:
            raise Http404()    

    def get(self, request, format=None):
        self.check_role(request)
        all_occupants= ReporteeProfile.objects.all()
        serializers = ReporteeSerializer(all_occupants, many=True)
        return Response(serializers.data) 



  #occupants API  List    

class OccupantList(APIView):
    def get(self, request, format=None):
        all_resident = OccupantListProfile.objects.all()
        serializers = OccupantSerializer(all_resident, many=True)
        return Response(serializers.data)


#Business API List
class BusinessList(APIView):
    def get(self, request, format=None):
        all_business = Business.objects.all()
        serializers = BusinessSerializer(all_business, many=True)
        return Response(serializers.data)
