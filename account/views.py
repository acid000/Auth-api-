from django.shortcuts import render
#user authentication system
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserregisterSerializer,UserLoginSerializer,UserprofileSerializer,UserPasswordChangeSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
#generating the tokens
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
#registering the user
class Userregister(APIView):

        def post(self, request, format=None):
                serializer=UserregisterSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                        user=serializer.save()
                        token=get_tokens_for_user(user)
                        return Response({'token':token,'msg':'user created'})


                return Response({'msg':'bhag madharchod'})
       
   # login the user    
class UserLoginView(APIView):
        def post(self,request,format=None):
                serializer=UserLoginSerializer(data=request.data)
                if serializer.is_valid(raise_exception=True):
                        email=serializer.data.get('email')
                        password=serializer.data.get('password')
                        user=authenticate(email=email,password=password)
                        if user is not None:
                            token=get_tokens_for_user(user)
                            return Response({'token':token,'msg':'login success'})
                        
                        else:
                               return Response({'errors':{'non_field_errors':['email or password is not valid']}})
                        

                return Response(serializer.errors)        
                                
    #view user                            
class UserprofileView(APIView):
       permission_classes=[IsAuthenticated]
       def get(self,request,format=None):
              serializer=UserprofileSerializer(request.user)
              return Response(serializer.data)

#change password
class UserPasswordChangeView(APIView):
       permission_classes=[IsAuthenticated]
       def post(self,request,format=None):
              serializer=UserPasswordChangeSerializer(data=request.data,context={'user':request.user})
              if serializer.is_valid(raise_exception=True):
                    return Response({'msg':'password changed sucessfully'})
              
              return Response({'msg':'did not changed'})
                                                            
