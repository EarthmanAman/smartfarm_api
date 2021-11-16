
from django.contrib import admin
from django.urls import path, include

from . views import CropList, Main, FarmerCropCreate, ChemicalList

app_name = "accounts"

urlpatterns = [
    path("crops", CropList.as_view(), name="crops"),
    path("chemicals", ChemicalList.as_view(), name="chemicals"),
    path("user/<int:pk>", Main.as_view(), name="main"),
    path("crops/create", FarmerCropCreate.as_view(), name="farmer_crop_create"),
]
