from django.core.urlresolvers import resolve
from django.utils.html import escape
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from unittest import skip
from records.forms import (
	RecordForm, EMPTY_ITEM_ERROR,
	DUPLICATE_ITEM_ERROR,ExistingArtistRecordForm,
	MinimalRecordForm,MinimalArtistForm
	)
from records.models import Record, Artist

from records.views import home_page

class RecordViewTest(TestCase):
	def test_for_invalid_input_renders_home_teplate(self):
		response = self.client.post('/records/new', data={'name':''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'home.html')
	# Need to decide which form will be used on home page
	@skip
	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/records/new', data={'name':'','artist':''})
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))
	
	def test_for_invalid_input_passes_form_to_template(self):
		response = self.client.post('/records/new', data={'name':''})
		self.assertIsInstance(response.context['form'],RecordForm)
	
	def test_displays_record_form(self):
		artist = Artist.objects.create(name='dédé')
		record = Record.objects.create(name="record1",ean=23344,artist=artist)
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
		
		
	def test_can_save_a_POST_request_to_an_existing_artist(self):
		artist = Artist.objects.create(name='artist1')
		correct_artist = Artist.objects.create(name='artist2')

		self.client.post(
			'/records/new',
			data = {
				'name': 'New Record on Existing Artist',
				'artist': correct_artist.id,
				'ean':711297880116,
				'year': 2015
			}
		)
			
		self.assertEqual(Record.objects.count(),1)
		new_item = Record.objects.first()
		self.assertEqual(new_item.name,'New Record on Existing Artist')
		self.assertEqual(new_item.artist, correct_artist)

	def test_POST_redirects_to_records_view(self):
		artist = Artist.objects.create(name='artist1')
		other_record = Record.objects.create(name="record1",artist=artist)
		correct_record = Record.objects.create(name="record2",artist=artist,ean=84160)
		response = self.client.post(
			'/records/%d/' % (correct_record.id),
			data={
			'name': correct_record.name,
			'artist': correct_record.artist.id,
			'ean':78418910918,
			'year':1987,
			}
		)
		last_record = Record.objects.last()
		self.assertRedirects(response,'/records/%d/' % (correct_record.id,))
		self.assertEqual(last_record.id,correct_record.id)
		

	def test_validation_errors_end_up_on_records_pages(self):
		artist = Artist.objects.create(name='artist1')
		record = Record.objects.create(artist=artist,name="record1")
		response = self.client.post(
			'/records/%d/' % (record.id,),
			data = {'name': '',
					'artist': artist.id}
		)
		self.assertEqual(response.status_code,200)
		self.assertTemplateUsed(response, 'record.html')
		expected_error = escape(EMPTY_ITEM_ERROR)
		self.assertContains(response, expected_error)

	def test_passes_correct_record_to_template(self):
		artist = Artist.objects.create(name='artist1')
		other_record = Record.objects.create(artist=artist,name="record1",ean=48181651)
		correct_record = Record.objects.create(artist=artist,name="record2",ean=5646845)
		response = self.client.get('/records/%d/' % (correct_record.id),)
		self.assertEqual(response.context['record'],correct_record)
	@skip
	def test_uses_list_template(self):
		artist = Artist.objects.create(name='artist1')
		record = Record.objects.create(artist=artist,name="record1")
		response = self.client.get('/records/%d/' % (record.id,))
		self.assertTemplateUsed(response,'record.html')

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
			'artist':artist1.id,
			'ean':545435456
			}
        	)
		self.assertEqual(Record.objects.count(), recordsNb+1)
		new_record = Record.objects.first()
		self.assertEqual(new_record.name, 'Records102')
	
	def test_redirects_after_POST(self):
		artist1 = Artist.objects.create(name='artist1')
		artist1.save()
		response = self.client.post(
			'/records/new',
			data={
			'name': 'Records102',
			'year':2010,
			'artist':artist1.id,
			'ean':545435458
			}
		)
		new_record = Record.objects.last()
		self.assertRedirects(response,'/records/%d/' % (new_record.id,))
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
	
	def test_new_list_only_saves_item_when_necessary(self):
		self.client.post(
			'/records/new',
			data={'name': ''}
		)
		self.assertEqual(Record.objects.count(), 0)	
		
class ArtistViewTest(TestCase):
	def test_displays_artist_full_desc(self):
		artist1 = Artist.objects.create(
			name='Prodigy'
		)
		artist1.save()
		response = self.client.get('/artists/%d/' % (artist1.id))
		self.assertContains(response, artist1.name)
		
	def test_displays_only_items_for_that_artist(self):
		first_artist = Artist.objects.create(name='artist1')
		Record.objects.create(name = 'item1',artist=first_artist,ean=12345)
		Record.objects.create(name = 'item2',artist=first_artist,ean=12346)
		second_artist = Artist.objects.create(name='artist2')
		Record.objects.create(name = 'item3',artist=second_artist,ean=12347)
		Record.objects.create(name = 'item4',artist=second_artist,ean=12348)
		
		response = self.client.get('/artists/%d/' % (first_artist.id,))
		
		self.assertContains(response,'item1')
		self.assertContains(response,'item2')
		self.assertNotContains(response,'item3')
		self.assertNotContains(response,'item4')
	def test_record_link_to_record_desc(self):
		first_artist = Artist.objects.create(name='artist1')
		Record.objects.create(name = 'item1',artist=first_artist,ean=12345)
		record2=Record.objects.create(name = 'item2',artist=first_artist,ean=12346)
		response = self.client.get('/artists/%d/' % (first_artist.id,))
		self.assertContains(response,'/records/%d/' % (record2.id))

class NewArtistTest(TestCase):
	def test_saving_POST_request(self):
		artistsNb = Artist.objects.count()
		self.client.post(
			'/artists/new',
			data={'name': 'The Prodigy'}
			)
		self.assertEqual(Artist.objects.count(),artistsNb+1)
	def test_invalid_form_redirect_home(self):
		response = self.client.post(
			'/artists/new',
			data={'name':''}
			)
		self.assertTemplateUsed(response,'home.html')
		
class HomePageTest(TestCase):

	def test_home_page_renders_home_template(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')
	
	def test_home_page_DONT_uses_record_form(self):
		response = self.client.get('/')
		self.assertNotIsInstance(response.context['minimalRecordForm'],RecordForm)

	def test_home_page_display_artists(self):
		artist1 = Artist.objects.create(name='artist1 with complicated String')
		artist1.save()
		response = self.client.get('/')
		self.assertContains(response,artist1.name)
	def test_home_page_display_quick_record_button(self):
		response = self.client.get('/')
		self.assertContains(response,'<button class="btn navbar-btn navbar-left" id="new_record" data-toggle="modal" data-target="#NewRecordModal">New Record</button>')
	def test_home_page_display_quick_artist_button(self):
		response = self.client.get('/')
		self.assertContains(response,'<button class="btn navbar-btn navbar-left" id="new_artist" data-toggle="modal" data-target="#NewArtistModal">New Artist</button>')
	def test_home_page_uses_quick_record_creation(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['minimalRecordForm'],MinimalRecordForm)
	def test_home_page_use_quick_artist_creation(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['minimalArtistForm'],MinimalArtistForm)


