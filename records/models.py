from django.db import models
from django.core.urlresolvers import reverse

class Artist(models.Model):
	name = models.TextField(blank=False)
	id = models.AutoField(primary_key=True)
	class Meta:
		ordering = ('id',)
	def __str__(self):
		return self.name
	def get_absolute_url(self):
		return reverse('view_artist',args=[self.id])
	def records_set(self):
		return Record.objects.filter(artist=self)
		
class Record(models.Model):
	name = models.TextField(default='')
	ean = models.BigIntegerField(
		unique=True,
		null=True,
		blank=False,
		verbose_name='EAN Code or any code that could identify the Item',
	)
	year = models.PositiveSmallIntegerField(
		default=2000,
		blank=True,
		null=True
		)
	artist = models.ForeignKey(
		'Artist',
		blank=False,
		related_name='records',
		)
	id = models.AutoField(primary_key=True)
	class Meta:
		ordering = ('id',)
		unique_together = ('artist','name')
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('view_record',args=[self.id])
