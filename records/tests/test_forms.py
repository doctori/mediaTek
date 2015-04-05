from django.test import TestCase
from unittest import skip
from records.forms import (
	ArtistForm,RecordForm, EMPTY_ITEM_ERROR,
	DUPLICATE_ITEM_ERROR,ExistingArtistRecordForm,
	MinimalRecordForm
	)
from records.models import Record, Artist

class RecordFormTest(TestCase):
	
	def test_form_renders_item_text_input(self):
		form = RecordForm()
		self.assertIn('placeholder="Name of the Record"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

	def test_form_validation_for_blank_items(self):
		form = RecordForm(data={
			'name':'',
			'year':'',
			'artist':'',
			'ean':''})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['name'],
			[EMPTY_ITEM_ERROR]
		)
	def test_form_save_handles_saving_record_for_an_artist(self):
		artist = Artist.objects.create(name='artist1')
		form = ExistingArtistRecordForm(data={
			'name':'save me',
			'year':2010,
			'artist':artist.id,
			'ean':545435456})
		new_record = form.save()
		self.assertEqual(new_record, Record.objects.last())
		self.assertEqual(new_record.name, 'save me')
		
class ExistingRecordFormTest(TestCase):
	
	def test_form_renders_item_text_input(self):
		artist = Artist.objects.create(name='artist1')
		artist.save()
		record = Record.objects.create(
			name='record2',
			artist= artist,
			ean='12345',)
		form = ExistingArtistRecordForm(instance=record)
		self.assertIn('placeholder="Name of the Record"', form.as_p())
	
	def test_form_save_new_record(self):
		artist = Artist.objects.create(name='artist1')
		artist.save()
		form = RecordForm(data={
			'name':'save me',
			'year':2010,
			'artist':artist.id,
			'ean':545435456},
			)
		new_record = form.save()
		self.assertEqual(new_record, Record.objects.last())
	@skip
	def test_form_validation_for_blank_items(self):
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_,data={'text':''})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['text'],
			[EMPTY_ITEM_ERROR]
		)
	@skip
	def test_form_validation_for_duplicate_items(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_,text='Am I Unique ?')
		form = ExistingListItemForm(for_list=list_,data={'text':'Am I Unique ?'})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'],[DUPLICATE_ITEM_ERROR])

class ArtistFormTest(TestCase):
	def test_form_render_artist_text_input(self):
		form = ArtistForm()
		self.assertIn('placeholder="Name of the Artist"',form.as_p())
		self.assertIn('class="form-control input-lg"',form.as_p())
	
	def test_form_validation_for_blank_items(self):
		form = ArtistForm(data={
			'name':'',
			})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['name'],
			[EMPTY_ITEM_ERROR]
		)
	def test_save_handles_saving_artist(self):
		form = ArtistForm(data={
			'name':'The Prodigy'
			})
		new_artist=form.save()
		self.assertEqual(new_artist, Artist.objects.last())
		self.assertEqual(new_artist.name, 'The Prodigy')
class MinimalRecordFormTest(TestCase):
	def test_form_render_record_input(self):
		form = MinimalRecordForm()
		self.assertIn('placeholder="Name of the Record"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())


