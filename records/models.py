from django.db import models
from django.core.urlresolvers import reverse

class Artist(models.Model):
	name = models.TextField(default='')
	class Meta:
		ordering = ('id',)
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('view_artist',args=[self.id])
		
class Record(models.Model):
	name = models.TextField(default='')
	artist = models.ForeignKey(Artist,default=None)
	
	class Meta:
		ordering = ('id',)
		unique_together = ('artist','name')
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('view_record',args=[self.id])
