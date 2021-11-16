from django.db import models
from django.contrib.auth.models import User

from versatileimagefield.fields import VersatileImageField, PPOIField
class Image(models.Model):
    
    name     = models.CharField(max_length=255)
   
    image = VersatileImageField(
       
     'Image',
       
      upload_to='images/',
       
       ppoi_field='image_ppoi'
        )
   
    image_ppoi = PPOIField()

    
    def __str__(self):
        return self.name

class Crop(models.Model):
	name 	= models.CharField(max_length=100, unique=True)
	desc 	= models.TextField(blank=True, null=True)
	image = models.ImageField(
	    upload_to="images/",
	    blank=True,
	    null=True,
	)

	def __str__(self):
	    return self.name

class QuickGuide(models.Model):
	crop 	= models.ForeignKey(Crop, on_delete=models.CASCADE, blank=True, null=True)
	name 	= models.CharField(max_length=50)
	desc	= models.TextField()
	icon 	= models.CharField(max_length=50, blank=True, null=True)
	icon_color 	= models.CharField(max_length=50, blank=True, null=True)

	def __str__(self):
		return self.name + " " + self.crop.__str__()

class FarmerCrop(models.Model):
	user 	= models.ForeignKey(User, on_delete=models.CASCADE)
	crop 	= models.ForeignKey(Crop, on_delete=models.CASCADE)
	date 	= models.DateField()

	def __str__(self):
		return self.user.email + " - " + self.crop.name + " - " + str(self.date)

class Schedule(models.Model):
	crop 		= models.ForeignKey(Crop, on_delete=models.CASCADE)
	days 		= models.IntegerField()
	name        = models.CharField(max_length=100, blank=True, null=True)
	activity 	= models.TextField()
	
	def __str__(self):
		return self.crop.name + " - " + self.name + " - " + str(self.days)

class CropSchedule(models.Model):
	farmer_crop 	= models.ForeignKey(FarmerCrop, on_delete=models.CASCADE)
	schedule 		= models.ForeignKey(Schedule, on_delete=models.CASCADE)
	done 			= models.BooleanField(default=False)
	date 			= models.DateField(blank=True, null=True)

class Chemical(models.Model):
	name 			= models.CharField(max_length=100)
	instructions 	= models.TextField()
	link 			= models.CharField(max_length=500, blank=True, null=True)
	image 			= models.ImageField(
					    upload_to="images/",
					    blank=True,
					    null=True,
					)
	def __str__(self):
		return self.name
        
class CropChemical(models.Model):
	crop 		= models.ForeignKey(Crop, on_delete=models.CASCADE)
	chemical 	= models.ForeignKey(Chemical, on_delete=models.CASCADE)

	def __str__(self):
		return self.crop.name + " - "+ self.chemical.name

class ChemicalSchedule(models.Model):
	schedule 		= models.ForeignKey(Schedule, on_delete=models.CASCADE)
	crop_chemical 	= models.ForeignKey(CropChemical, on_delete=models.CASCADE)

	def __str__(self):
		return self.schedule.name + " - " + self.crop_chemical.chemical.name
