from django.test import TestCase
from unittest import skip
from records.forms import (
	RecordForm, EMPTY_ITEM_ERROR,
	DUPLICATE_ITEM_ERROR,ExistingRecordItemForm
	)
from records.models import Record, Artist

class RecordFormTest(TestCase):
	
	def test_form_renders_item_text_input(self):
		form = RecordForm()
		self.assertIn('placeholder="Name of the Record"', form.as_p())
		self.assertIn('class="form-control input-lg"', form.as_p())

	def test_form_validation_for_blank_items(self):
		form = RecordForm(data={'name':''})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['name'],
			[EMPTY_ITEM_ERROR]
		)
	def test_form_save_handles_saving_item_to_a_list(self):
		artist = Artist.objects.create(name='artist1')
		form = RecordForm(data={'name':'save me'})
		new_item = form.save(for_artist=artist)
		self.assertEqual(new_item, Record.objects.first())
		self.assertEqual(new_item.name, 'save me')
		self.assertEqual(new_item.artist, artist)
@skip
class ExistingListItemFormTest(TestCase):
	
	def test_form_renders_item_text_input(self):
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_)
		self.assertIn('placeholder="Enter a to-do item"', form.as_p())
	def test_form_save(self):
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_, data={'text':'save me!'})
		new_item = form.save()
		self.assertEqual(new_item, Item.objects.all()[0])
		
	def test_form_validation_for_blank_items(self):
		list_ = List.objects.create()
		form = ExistingListItemForm(for_list=list_,data={'text':''})
		self.assertFalse(form.is_valid())
		self.assertEqual(
			form.errors['text'],
			[EMPTY_ITEM_ERROR]
		)
	def test_form_validation_for_duplicate_items(self):
		list_ = List.objects.create()
		Item.objects.create(list=list_,text='Am I Unique ?')
		form = ExistingListItemForm(for_list=list_,data={'text':'Am I Unique ?'})
		self.assertFalse(form.is_valid())
		self.assertEqual(form.errors['text'],[DUPLICATE_ITEM_ERROR])
		