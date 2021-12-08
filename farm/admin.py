from django.contrib import admin

from . models import (
	Crop,
	FarmerCrop,
	Schedule,
	Chemical,
	CropChemical,
	ChemicalSchedule,
	CropSchedule,
	QuickGuide
)
#psycopg2==2.7.5
admin.site.register(Crop)
admin.site.register(FarmerCrop)
admin.site.register(Schedule)
admin.site.register(Chemical)
admin.site.register(CropChemical)
admin.site.register(ChemicalSchedule)
admin.site.register(CropSchedule)
admin.site.register(QuickGuide)
