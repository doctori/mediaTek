from django.db import models
from django.core.urlresolvers import reverse

class Artist(models.Model):
	name = models.TextField(default='')
	id = models.AutoField(primary_key=True)
	class Meta:
		ordering = ('id',)
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('view_artist',args=[self.id])
		
class Record(models.Model):
	name = models.TextField(default='')
	ean = models.BigIntegerField(
		unique=True,
		blank=False,
		verbose_name='EAN Code or any code that could identify the Item',
		default=0)
	year = models.PositiveSmallIntegerField(default=2000)
	artist = models.TextField(
	blank=False
	)
	id = models.AutoField(primary_key=True)
	class Meta:
		ordering = ('id',)
		#unique_together = ('artist','name')
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('view_record',args=[self.id])
