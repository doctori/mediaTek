from django.core.urlresolvers import resolve
from django.test import TestCase
from django.core.exceptions import ValidationError

from lists.models import Record, Artist

from lists.views import home_page

class ArtistAndRecordsModelsTest(TestCase):
	
	def test_default_text(self):
		record = Record()
		self.assertEqual(record.name, '')
	
	def test_record_is_related_to_artist(self):
		artist = Artist.objects.create(name='artist1')
		record = Record()
		record.artist = artist
		record.save()
		self.assertIn(record, artist.record_set.all())
	
	def test_cannot_save_empty_artist_name(self):
		artist = Artist.objects.create(name='')
		with self.assertRaises(ValidationError):
			artist.save()
			artist.full_clean()
			
	def test_cannot_save_empty_artist_item(self):
		artist = Artist.objects.create(name='artist1')
		record = Record(artist=artist,name='')
		with self.assertRaises(ValidationError):
			record.save()
			record.full_clean()
			
	def test_duplicate_records_are_invalid(self):
		artist = Artist.objects.create(name='artist1')
		Record.objects.create(artist=artist, name='Am I Unique ?')
		with self.assertRaises(ValidationError):
			record = Record(artist=artist, name='Am I Unique ?')
			record.full_clean()
	def test_CAN_save_item_to_different_lists(self):
		artist1 = Artist.objects.create(name='artist1')
		artist2 = Artist.objects.create(name='artist2')
		Record.objects.create(artist=artist1, name='Am I Unique ?')
		record2 = Record(artist=artist2, name='Am I Unique ?')
		record2.full_clean() #Should pass
		
	def test_artist_ordering(self):
		artist1 = List.objects.create(name='artist1')
		item1 = Record.objects.create(artist=artist1, name='Am I The First ?')
		item2 = Record.objects.create(artist=artist1, name='1 and Only')
		item3 = Record.objects.create(artist=artist1, name='Z I\'m always the last')
		self.assertEqual(
			list(Item.objects.all()),
			[item1,item2,item3]
		)
		
	def test_string_representation(self):
		artist = Artist.objects.create(name='artist1')
		record = Record(artist=artist,name='Am I readable ?')
		self.assertEqual(str(record),'Am I readable ?')
		
class RecordModelTest(TestCase):
	def test_get_absolute_url(self):
		artist = Artist.objects.create(name='artist1')
		record = Record(artist=artist,name='Am I readable ?')
		self.assertEqual(list_.get_absolute_url(), '/records/%d/' % (list_.id,))
	
