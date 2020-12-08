
from django.shortcuts import render, redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import *
# from rest_framework.generics import ListCreateAPIView,RetrieveUpdateDestroyAPIView

from .models import SuperuserProfile,AdminProfile,Business,Neighborhood
from .serializer import *
from django.conf import settings
# from rest_framework import viewsets
# Create your views here.


#user accessibility
def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def welcome(request):

    return redirect('api/users')


#Superuser apis
class SuperuserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def check_role(self, request):
        if request.user.is_superuser:
            pass
        else:
            raise Http404()       
    
    def get_superuser(self, pk):
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
        this_superuser = self.get_superuser(pk)
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
        all_occupants= OccupantProfile.objects.all()
        serializers = OccupantsSerializer(all_occupants, many=True)
        return Response(serializers.data) 



class NeighborhoodView(APIView):
    permission_classes=(IsAuthenticated,)
    def post(self, request):
        serializer = NeighborhoodSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

     
    def get_hood(self, request):
        try:
            hood_id = request.GET.get('hood_id')
                
            return Neighborhood.objects.filter(id = hood_id).first()
        except Neighborhood.DoesNotExist:
            raise Http404()


    

    def get(self, request):
        if request.GET.get('hood_id', None):
            hood_id = request.GET.get('hood_id')
            hood = self.get_hood(request)
            if hood != None:
                serializers = NeighborhoodSerializer(data=request.data)
                return Response(serializers.data)
            return Response({'detail':'no neighbourhood with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request):
        if request.GET.get('hood_id', None):
            hood = self.get_hood(request)
            if hood != None:
                serializers = NeighborSerializer(data=request.data)

                if serializers.is_valid():
                    serializers.save()
                    return Response(serializers.data)
                else:
                    return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'detail':'no neighbourhood  with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request):
        if request.GET.get('hood_id', None):
            hood = self.get_hood(request)
            if hood != None:
                hood.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            return Response({'detail':'no hood with that id'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail':'no hood id provided'}, status=status.HTTP_400_BAD_REQUEST)

       


  #occupants API  List    

class OccupantList(APIView):
    def get(self, request, format=None):
        all_resident = OccupantListProfile.objects.all()
        serializers = OccupantsSerializer(all_occupants, many=True)
        return Response(serializers.data)


    def post(self, request, format=None):
            serializers = OccupantSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


#Business API List
class BusinessList(APIView):
    def get(self, request, format=None):
        all_business = Business.objects.all()
        serializers = BusinessSerializer(all_business, many=True)
        return Response(serializers.data)


    def post(self, request, format=None):
            serializers = BusinessSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save()
                return Response(serializers.data, status=status.HTTP_201_CREATED)
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)




class PostList(APIView):
    def get(self, request, format=None):
        all_post = Post.objects.all()
        serializers = PostSerializer(all_post, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = PostSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentList(APIView):

    def get(self, request, format=None):
        all_comments = Comment.objects.all()
        serializers = CommentSerializer(all_comments, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = CommentSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class NeighborhoodList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        
        all_hoods = Neighborhood.objects.all()
        serializers = NeighborhoodSerializer(all_hoods, many=True)
        return Response(serializers.data)
