import random
from django.contrib.auth.models import User
from django.conf import settings
from rest_framework.authtoken.models import Token
from rest_framework.serializers import (
	EmailField,
	CharField,
	HyperlinkedIdentityField,
	ModelSerializer, 
	SerializerMethodField,
	ListField,
	Serializer,

	ValidationError,	
	)

class ChangePasswordSerializer(Serializer):
	model = User

	"""
	Serializer for password change endpoint.
	"""
	old_password = CharField(required=True)
	new_password = CharField(required=True)

class UserCreateSer(ModelSerializer):

	"""
		Description
		-------------
			* Serializer for the User Model
			* Handle creation of users

		Variables
		----------
			* email
			* email2

		Fields
		---------
			email
			email2
			first_name
			last_name
			password

		Methods
		--------
			* def validate_email2(self, value) = validate if email are equal
			* def create(self, data) = handle creation

	"""

	email = EmailField(label="Email Address")
	confirm_email = EmailField(label="Confirm Email")

	class Meta:
		model = User
		fields = [
			"username",
			'email',
			'confirm_email',
			'first_name',
			'last_name',
			'password',
		]

		extra_kwargs = {'password':
			{"write_only":True}
		}
	
	def validate_confirm_email(self, value):
		data = self.get_initial()
		email = data.get('email')
		confirm_email = value

		if email != confirm_email:
			raise ValidationError("Emails Must Match.")

		user_qs = User.objects.filter(email=email)
		if user_qs.exists():
			raise ValidationError("This email is already registered.")
		return value

	def create(self, validated_data):
		username = validated_data['username']
		email = validated_data['confirm_email']
		password = validated_data['password']
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		user = User(username=username, email=email, first_name=first_name, last_name=last_name)
		user.set_password(password)
		user.save()
		return validated_data

class UserUpdateSer(ModelSerializer):

	class Meta:
		model = User
		fields = [
			"username",
			'email',
			'first_name',
			'last_name',
		]