from django.db import models

# Create your models here.

class Post(models.Model):
	title = models.CharField(max_length=150)
	text = models.TextField()

	def __str__(self):
		return self.title

class City(models.Model):
	name = models.CharField(max_length=100, help_text="O'zbekcha nomi")
	city = models.CharField(max_length=100, help_text="Inglizcha nomi")
	lat = models.FloatField(help_text="latitude - geografik kenglik")
	lon = models.FloatField(help_text="longitude - geografik uzunlik")

	def __str__(self):
		return self.city