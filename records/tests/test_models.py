from django.core.urlresolvers import resolve
from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from unittest import skip
from records.models import Record, Artist

from records.views import home_page

class ArtistAndRecordsModelsTest(TestCase):
	
	def test_default_text(self):
		record = Record()
		self.assertEqual(record.name, '')
		
	def test_record_attributes_are_created(self):
		artist1 = Artist.objects.create(
			name = 'The Prodigy'
		)
		record = Record(
			name = 'Invaders Must Die',
			artist = artist1,
			year = 2012,
			ean = 711297880113)
		record.save()
		self.assertIn(record.name,'Invaders Must Die')
		self.assertIn(record.artist.name,'The Prodigy')
		self.assertIn(str(record.year),'2012')
		self.assertIn(str(record.ean),str(711297880113))
		
	def test_record_ean_is_unique(self):
		artist1 = Artist.objects.create(
			name = 'The Prodigy'
		)
		record1 = Record(
			name = 'Invaders Must Die',
			artist = artist1,
			year = 2012,
			ean = 711297880114)
		record1.save()
		record1.full_clean()
		
		record2 = Record(
			name = 'Invaders Must Dive',
			artist = artist1,
			year = 2016,
			ean = 711297880114)
		with self.assertRaises(IntegrityError):
			record2.save()
			
	def test_record_is_related_to_artist(self):
		artist1 = Artist.objects.create(name='artist1')
		artist1.save()
		record = Record(
			name = 'Invaders Must Dive',
			artist = artist1,
			year = 2016,
			ean = 711297880114
		)
		record.save()
		self.assertIn(record, artist1.records_set())

	def test_record_artist_is_object_artist(self):
		artist1 = Artist.objects.create(name='artist1')
		artist1.save()
		record = Record(
			name = 'Invaders Must Dive',
			artist = artist1,
			year = 2016,
			ean = 711297880114
		)
		record.save()
		record.full_clean()
		self.assertEqual(type(artist1),type(Record.objects.last().artist))
		
	def test_cannot_save_empty_artist_in_record(self):
		artist = Artist.objects.create(name='')
		record = Record(
			name = 'Invaders Must Dive',
			year = 2016,
			ean = 711297880114)
		with self.assertRaises(IntegrityError):
			record.save()
			record.full_clean()
	def test_cannot_save_empty_ean_in_record(self):
		artist = Artist.objects.create(name='The Prodigy')
		record = Record(
			name = 'Invaders Must Dive',
			artist = artist,
			year = 2016)
		with self.assertRaises(ValidationError):
			record.save()
			record.full_clean()

	def test_cannot_save_empty_artist_name(self):
		artist = Artist.objects.create(name='')
		with self.assertRaises(ValidationError):
			artist.save()
			artist.full_clean()
	@skip	
	def test_cannot_save_empty_artist_item(self):
		artist1 = Artist.objects.create(name='artist1')
		record = Record(artist=artist1,name='')
		with self.assertRaises(ValidationError):
			record.save()
			record.full_clean()
			
	def test_duplicate_records_are_invalid(self):
		artist1 = Artist.objects.create(name='artist1')
		Record.objects.create(
			artist=artist1,
			name='Am I Unique ?',
			year = 2016,
			ean = 23213230
			)
		with self.assertRaises(IntegrityError):
			record = Record.objects.create(
			artist=artist1,
			name='Am I Unique ?',
			year = 2016,
			ean = 23213230
			)
			record.full_clean()
	
	def test_CAN_save_records_to_different_artists(self):
		artist1 = Artist.objects.create(name='artist1')
		artist2 = Artist.objects.create(name='artist2')
		Record.objects.create(
			artist=artist1,
			name='Am I Unique ?',
			year = 2016,
			ean = 232132121243
			)
		record2 = Record(artist=artist2,
			name='Am I Unique ?',
			year = 2016,
			ean = 232132121323)
		record2.full_clean() #Should pass
	

	def test_artist_ordering(self):
		artist1 = Artist.objects.create(name='artist1')
		item1 = Record.objects.create(
			artist=artist1,
			name='Am I The First ?',
			year = 2016,
			ean = 23213230
			)
		item2 = Record.objects.create(
			artist=artist1,
			name='1 and Only',
			year = 2018,
			ean = 23213231)
		item3 = Record.objects.create(
			artist=artist1,
			name='Z I\'m always the last',
			year = 2001,
			ean = 23213219
			)
		self.assertEqual(
			list(Record.objects.all()),
			[item1,item2,item3]
		)

	
		
class RecordModelTest(TestCase):
	def test_get_absolute_url(self):
		artist = Artist.objects.create(name='artist1')
		record = Record.objects.create(name='Am I readable ?',artist=artist)
		self.assertEqual(record.get_absolute_url(), '/records/%d/' % (record.id,))
	
	def test_string_representation(self):
		artist = Artist.objects.create(name='artist1')
		record = Record.objects.create(
			artist=artist,
			name='Am I readable ?',
			year = 2016,
			ean = 23213230)
		self.assertEqual(str(record),'Am I readable ?')
	
