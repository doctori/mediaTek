from .base import FunctionalTest
from unittest import skip
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class RecordValidationTest(FunctionalTest):
	def get_error_element(self):
		return self.browser.find_element_by_css_selector('.has-error')
		
	def test_error_messages_are_cleared_on_input(self):
		#Creation d'un vinyle qui genère une erreur :
		self.browser.get(self.server_url)
		self.get_record_input_box().send_keys('\n')
		error = self.get_error_element()
		self.assertTrue(error.is_displayed())
		
		#l'utilisateur corrige l'erreur
		self.get_record_input_box().send_keys('yeah sorry')
		error = self.get_error_element()
		self.assertFalse(error.is_displayed())
		
	def test_cannot_add_empty_list_item(self):
		#L'utilisateur arrive sur la page principale et essaye d'ajouter un item vide
		# il appuie sur entrÉ
		self.browser.get(self.server_url)
		self.get_record_input_box().send_keys('\n')	
		
		#rafraichissement de la page principale avec un message d'erreur
		error = self.get_error_element()
		self.assertEqual(error.text, 'Impossible d\'avoir un élement Vide')
		
		#L'utilisateur saisi maintenant une valeur correcte et appuie sur entré et ça fonctionne normalement
		self.get_item_input_box().send_keys('Invaders Must Die\n')	
		# Il arrive sur une page qui lui demande plus d'informations
		recordCreationUrl = self.browser.current_url
		self.assertRegex(recordCreationUrl, '/records/.+')
		self.add_record('Invaders Must Die',2012,'Prodigy',711297880113)

		# l'utilisateur essaye encore de saisir un champ vide
		self.get_item_input_box().send_keys('\n')
		
		# le même message d'erreur que la premiere fois est affiché
		error = self.get_error_element()
		self.assertEqual(error.text, 'Impossible d\'avoir un élement Vide')
		
	def test_cannot_add_duplicate_items(self):
		#L'utilisateur est sur la page d'accueil et saisi une nouvelle liste
		self.browser.get(self.server_url)
		self.get_item_input_box().send_keys('Invaders Must Die\n')	
		self.add_record('Invaders Must Die',2012,'Prodigy',711297880113)
		
		self.get_item_input_box().send_keys('Invaders Must Die\n')	
		self.add_record('Invaders Must Die',2012,'Prodigy',711297880113)
		
		#L'utilisateur reçoit un message d'avertissement sur le fait que l'element existe déjà
		error = self.get_error_element()
		self.assertEqual(error.text, "L'element existe déjà")

