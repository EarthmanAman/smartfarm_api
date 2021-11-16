import datetime
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.generics import (
	CreateAPIView,
	ListAPIView,
	ListCreateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	UpdateAPIView,

	)

from . serializers import CropListSer, MainSer, FarmerCropCreateSer, ChemicalSer

from . models import Crop, FarmerCrop, CropSchedule, Schedule, Chemical

class CropList(ListAPIView):
	serializer_class = CropListSer
	queryset = Crop.objects.all()

class ChemicalList(ListAPIView):
	serializer_class = ChemicalSer
	queryset = Chemical.objects.all()

class Main(RetrieveAPIView):
	serializer_class = MainSer
	queryset = User.objects.all()

class FarmerCropCreate(CreateAPIView):
	serializer_class = FarmerCropCreateSer
	queryset = FarmerCrop.objects.all()

	def post(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)
		data =serializer.save()
		
		crop = Crop.objects.get(pk=request.data["crop"])
		schedules = Schedule.objects.filter(crop=crop)
		for schedule in schedules:
			date = data.date +  datetime.timedelta(days=schedule.days)
			crop_schedule = CropSchedule.objects.create(farmer_crop=data, schedule=schedule, date=date)
		
		return Response({
				"status":201,
			})