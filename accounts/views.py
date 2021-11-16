from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.status import (
	HTTP_400_BAD_REQUEST,
	HTTP_201_CREATED,
	HTTP_200_OK
	)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	ListCreateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,
	)
from . serializers import UserCreateSer, ChangePasswordSerializer, UserUpdateSer

class CustomAuthToken(ObtainAuthToken):

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data,
		                               context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']

		token= Token.objects.get(user=user)
		data = {}
		data["id"] = user.id
		data["email"] = user.email
		data["first_name"] = user.first_name
		data["last_name"] = user.last_name
		message = "Logged in successfully"
		return Response({
			"status": "success",
			"status_code": 201,
			"id": user.id,
            'message': message,
      		"data":data,
            "token": token.key,
		})

class UserUpdate(RetrieveUpdateAPIView):
	serializer_class = UserUpdateSer
	queryset = User.objects.all()

class UserCreate(CreateAPIView):
	"""
		Description
		-------------
			* A view which allow creation of a user 

		Methods
		---------
			* create(...) - overide the inbuilt create function 
							to enable returning a token to the user

		Improvements
		---------------
			* Access the user instance without fetching it from the db
	"""
	serializer_class = UserCreateSer
	queryset = User.objects.all()

	def create(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		token = None
		data = {}
		message = None
		status_code = HTTP_400_BAD_REQUEST
		status = "fail"

		if serializer.is_valid():

			# Obtain user data
			user_data = serializer.save()
			
			user = get_object_or_404(User, username=user_data["username"])

			# Obtain token
			token = get_object_or_404(Token, user=user).key 

			status_code = HTTP_201_CREATED
			# Formulating the response
			message = 'Registration successful'
			data["id"] = user.id
			data["email"] = user_data["email"]
			data["first_name"] = user_data["first_name"]
			data["last_name"] = user_data["last_name"]
			status = "success"
			


			return Response({
				"status": status,
				"id": user.id,
				"status_code": status_code,
	            'message': message,
	      		"data":data,
	            "token": token,
	        })
		else:
			message = 'Registration unsuccessful'
			errors = serializer.errors

			return Response({
				"status": status,
				"status_code": status_code,
	            'message': message,
	      		"errors":errors,
	     
	        })

class ChangePasswordView(UpdateAPIView):
	"""
	An endpoint for changing password.
	"""
	serializer_class = ChangePasswordSerializer
	model = User
	permission_classes = (AllowAny,)

	def get_object(self, queryset=None):
		obj = User.objects.get(pk=int(self.kwargs["pk"]))
		return obj

	def update(self, request, *args, **kwargs):
		self.object = self.get_object()
		serializer = self.get_serializer(data=request.data)

		if serializer.is_valid():
			# Check old password
			if not self.object.check_password(serializer.data.get("old_password")):
			    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
			# set_password also hashes the password that the user will get
			self.object.set_password(serializer.data.get("new_password"))
			self.object.save()
			response = {
			    'status': 'success',
			    'code': HTTP_200_OK,
			    'message': 'Password updated successfully',
			    'data': []
			}

			return Response(response)

		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
