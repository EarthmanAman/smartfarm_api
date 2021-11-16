import random
import datetime
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
from  versatileimagefield.serializers import VersatileImageFieldSerializer
from . models import (
    Crop, 
    Image, 
    FarmerCrop,
    CropSchedule,
    Schedule,
    Chemical,
    CropChemical,
    ChemicalSchedule,
    QuickGuide
    )


class QuickGuideSer(ModelSerializer):
    class Meta:
        model = QuickGuide
        fields = [
            "id",
            "name",
            "desc",
            "icon",
        ]

class CropListSer(ModelSerializer):
    quick_guides = SerializerMethodField()

    class Meta:
        model = Crop
        fields = [
			'id',
			"name",
            "desc",
			"image",
            "quick_guides",
		]
    def get_quick_guides(self, obj):
        return QuickGuideSer(obj.quickguide_set.all(), many=True).data


class ChemicalSer(ModelSerializer):
     
    class Meta:
        model = Chemical
        fields = [
            "id",
            "name",
            "instructions",
            "link",
            "image"

        ]

    
class CropChemicalSer(ModelSerializer):
    chemical = SerializerMethodField()
    class Meta:
        model = ChemicalSchedule
        fields = [
            "chemical",
        ]

    def get_chemical(self, obj):
        return ChemicalSer(obj.crop_chemical.chemical).data

class ScheduleSer(ModelSerializer):
    chemical = SerializerMethodField()
    crop = SerializerMethodField()
    class Meta:
        model = Schedule
        fields = [
            "id",
            "name",
            "days",
            "activity",
            "chemical",
            "crop",
        ]

    def get_chemical(self, obj):
        return CropChemicalSer(obj.chemicalschedule_set.all(), many=True).data
    def get_crop(self, obj):
        return CropListSer(obj.crop).data

class CropScheduleSer(ModelSerializer):
    schedule = SerializerMethodField()
    date = SerializerMethodField()    
    class Meta:
        model = CropSchedule
        fields = [
            "id",
            "schedule",
            "done",
            "date",
            
        ]

    def get_date(self, obj):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        date = obj.date
        if date:
            date_dict = {
                "full":date,
                "month": months[date.month - 1],
                "day": date.day,
                "weekday": days[date.weekday()],
            }
            return date_dict
        else:
            return None
    def get_schedule(self,obj):
        return ScheduleSer(obj.schedule).data

class FarmerCropSer(ModelSerializer):
    crop = SerializerMethodField()
    schedule =  SerializerMethodField()
    statistics = SerializerMethodField()
    schedule_dis = SerializerMethodField()
    class Meta:
        model = FarmerCrop
        fields = [
            "id",
            "crop",
            "schedule",
            "date",
            "statistics",
            "schedule_dis",
        ]

    def get_crop(self, obj):
        return CropListSer(obj.crop).data

    def get_schedule(self, obj):
        return CropScheduleSer(obj.cropschedule_set.all(), many=True).data

    def get_schedule_dis(self, obj):
        schedules = obj.cropschedule_set.all()
        dis = {}
        dates = []
        for schedule in schedules:
            if schedule.date in dates:
                dis[str(schedule.date)].append({"name":schedule.schedule.name})
            else:
                dis[str(schedule.date)] = [{"name":schedule.schedule.name}]
                dates.append(schedule.date)
        return dis

    def get_statistics(self, obj):
        completed = obj.cropschedule_set.filter(done=True).count()
        uncompleted = obj.cropschedule_set.filter(done=False).count()
        completed_perc = abs((completed / (completed + uncompleted)) * 100)
        uncompleted_perc = abs((uncompleted / (completed + uncompleted)) * 100)
        d = {
            "completed":completed,
            "uncompleted":uncompleted,
            "completed_perc":completed_perc,
            "uncompleted_perc":uncompleted_perc,
        }

        return d

class MainSer(ModelSerializer):
    crops = SerializerMethodField()
    my_chemicals = SerializerMethodField()
    my_schedules = SerializerMethodField()
    main_schedule = SerializerMethodField()
    schedule_dis = SerializerMethodField()
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "crops",
            "my_chemicals",
            "my_schedules",
            "main_schedule",
            "schedule_dis",
        ]

    def get_main_schedule(self, obj):
        crop_schedules = CropSchedule.objects.filter(farmer_crop__user=obj)
        if crop_schedules.exists():
            return CropScheduleSer(crop_schedules[0]).data
        return None
    def get_crops(self, obj):
        return FarmerCropSer(obj.farmercrop_set.all(), many=True).data

    def get_my_schedules(self, obj):
        crop_schedules = CropSchedule.objects.filter(farmer_crop__user=obj)
        return CropScheduleSer(crop_schedules, many=True).data

    def get_my_chemicals(self, obj):
        crop_schedules = CropSchedule.objects.filter(farmer_crop__user=obj)
        chemicals = []
        chem_ids = []
        for crop_schedule in crop_schedules:
            if crop_schedule.schedule.chemicalschedule_set.count() > 0:
                chems = crop_schedule.schedule.chemicalschedule_set.all()
                for chem in chems:
                    if chem.crop_chemical.chemical.id not in chem_ids:
                        chem_ids.append(chem.crop_chemical.chemical.id)
                        chemicals.append(chem.crop_chemical.chemical)
        return ChemicalSer(chemicals, many=True).data

    def get_schedule_dis(self, obj):
        schedules = CropSchedule.objects.filter(farmer_crop__user=obj)
        dis = {}
        dates = []
        for schedule in schedules:
            if schedule.date in dates:
                dis[str(schedule.date)].append({"name":schedule.schedule.name})
            else:
                dis[str(schedule.date)] = [{"name":schedule.schedule.name}]
                dates.append(schedule.date)
        return dis
class FarmerCropCreateSer(ModelSerializer):

    class Meta:
        model = FarmerCrop
        fields = [
            "user",
            "crop",
            "date",
        ]