from django.core.urlresolvers import resolve
from django.utils.html import escape
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from unittest import skip
from records.forms import (
	RecordForm, EMPTY_ITEM_ERROR,
	DUPLICATE_ITEM_ERROR,ExistingArtistRecordForm
	)
from records.models import Record, Artist

from records.views import home_page

class RecordViewTest(TestCase):
	def test_for_invalid_input_renders_home_teplate(self):
		response = self.client.post('/records/new', data={'name':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
		
	def test_validation_errors_are_shown_on_home_page(self):
	
		response = self.client.post('/records/new', data={'name':'','artist':''})
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))
	
	def test_for_invalid_input_passes_form_to_template(self):
		response = self.client.post('/records/new', data={'name':''})
		self.assertIsInstance(response.context['form'],RecordForm)
	
	def test_displays_record_form(self):
		artist = Artist.objects.create(name='dédé')
		record = Record.objects.create(name="record1",artist=artist)
		response = self.client.get('/records/%d/' % (record.id,))
		self.assertIsInstance(response.context['form'], ExistingArtistRecordForm)
		self.assertContains(response, record.name)
	def test_displays_record_full_desc(self):
		artist1 = Artist.objects.create(
			name='Prodigy'
		)
		artist1.save()
		record = Record.objects.create(
			name="record1",
			year=2012,
			artist=artist1,
			ean=711297880113
			)
		response = self.client.get('/records/%d/' % (record.id,))
		self.assertContains(response, record.name)
		self.assertContains(response, record.year)
		self.assertContains(response, record.artist)
		self.assertContains(response, record.ean)
		
		
	#A voir après l'ajout de la gestion des artistes
	@skip
	def test_can_save_a_POST_request_to_an_existing_list(self):
		artist = Artist.objects.create(name='artist1')
		correct_artist = Artist.objects.create(name='artist2')

		self.client.post(
			'/artists/%d/' % (correct_artist.id,),
			data = {'name': 'New Record on Existing Artist'}
			)
			
		self.assertEqual(Record.objects.count(),1)
		new_item = Record.objects.first()
		self.assertEqual(new_item.text,'New Record on Existing List')
		self.assertEqual(new_item.list, correct_artist)
	@skip
	def test_POST_redirects_to_list_view(self):
		other_record = Record.objects.create(name="record1")
		correct_record = Record.objects.create(name="record2")
		response = self.client.post(
			'/records/%d/' % (correct_record.id),
			data={'name': 'record2'}
		)
		new_record = Record.objects.last()
		self.assertRedirects(response,'/records/%d/' % (correct_record.id,))
	@skip
	def test_validation_errors_end_up_on_lists_pages(self):
		artist = Artist.objects.create(name='artist1')
		record = Record.objects.create(artist=artist,name="record1")
		response = self.client.post(
			'/records/%d/' % (record.id,),
			data = {'name': '',
					'artist_id': artist.id}
		)
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response, 'record.html')
		expected_error = escape(EMPTY_ITEM_ERROR)
		self.assertContains(response, expected_error)
	@skip
	def test_passes_correct_list_to_template(self):
		artist = Artist.objects.create(name='artist1')
		other_record = Record.objects.create(artist=artist,name="record1")
		correct_record = Record.objects.create(artist=artist,name="record2")
		response = self.client.get('/records/%d/' % (correct_record.id),)
		self.assertEqual(response.context['record'],correct_record)
	@skip
	def test_uses_list_template(self):
		artist = Artist.objects.create(name='artist1')
		record = Record.objects.create(artist=artist,name="record1")
		response = self.client.get('/records/%d/' % (record.id,))
		self.assertTemplateUsed(response,'record.html')
	#After First ARtist Implementation
	@skip
	def test_displays_only_items_for_that_artist(self):
		artist = Artist.objects.create(name='artist1')
		first_record = List.objects.create()
		Item.objects.create(text = 'item1',list=first_list)
		Item.objects.create(text = 'item2',list=first_list)
		second_list = List.objects.create()
		Item.objects.create(text = 'item3',list=second_list)
		Item.objects.create(text = 'item4',list=second_list)
		
		response = self.client.get('/records/%d/' % (first_list.id,))
		
		self.assertContains(response,'item1')
		self.assertContains(response,'item2')
		self.assertNotContains(response,'item3')
		self.assertNotContains(response,'item4')
	@skip	
	def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
		artist = Artist.objects.create(name='artist1')
		record1 = Record.objects.create(artist=artist,name="record1")
		record2 = Record.objects.create(artist=artist,name="record2")
		response = self.client.post(
		'/records/%d/' % (record1.id,),
			data={'name': 'record1'}
		)
		self.assertContains(response, escape(DUPLICATE_ITEM_ERROR))
		self.assertTemplateUsed(response, 'record.html')
		self.assertEqual(Item.objects.all().count(),1)
		
class NewRecordTest(TestCase):
	def test_saving_a_POST_request(self):
		artist1 = Artist.objects.create(name='artist1')
		artist1.save()
		recordsNb = Record.objects.count()
		self.client.post(
			'/records/new',
			data={
			'name': 'Records102',
			'year':2010,
			'artist':artist1.id,
			'ean':545435456
			}
        )
		self.assertEqual(Record.objects.count(), recordsNb+1)
		new_record = Record.objects.first()
		self.assertEqual(new_record.name, 'Records102')
	@skip
	def test_redirects_after_POST(self):
		list_ = List.objects.create()
		response = self.client.post(
			'/records/new',
			data={'text': 'A new list Item'}
        )
		new_list = List.objects.last()
		self.assertRedirects(response,'/records/%d/' % (new_list.id,))
	@skip
	def test_for_invalid_input_renders_home_template(self):
		response = self.client.post('/records/new', data={'name':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
	@skip
	def test_for_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/records/new', data={'name':''})
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))
	@skip
	def post_invalid_input(self):
		record = Record.objects.create()
		return self.client.post(
			'/records/%d/' % (record.id,),
			data={'name':''}
		)
	@skip
	def test_for_invalid_input_passes_form_to_template(self):
		response = self.post_invalid_input()
		self.assertIsInstance(response.context['form'],ExistingListRecordForm)
	@skip
	def test_new_list_only_saves_item_when_necessary(self):
		self.client.post(
			'/records/new',
			data={'name': ''}
		)
		self.assertEqual(Item.objects.count(), 0)	
		
		
class HomePageTest(TestCase):

	def test_home_page_renders_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')
	
	def test_home_page_uses_record_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'],RecordForm)

	
		


