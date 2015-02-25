from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):
	def test_can_search_a_record_and_add_another(self):
		#accès a la page de garde
		self.browser.get(self.server_url)
		# le titre de la page est 'MediaTek' et le titre sur la page
		self.assertIn('MediaTek', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('MediaTek', header_text)
		#L'utilisateur veux chercher un vinyle
		searchBox = self.get_record_search_box()
		self.assertEqual(
			searchBox.get_attribute('placeholder'),
			'Search a Record'
		)
		#Il cherche "Prodigy"
		searchBox.send_keys('Prodigy')
		#Après avoir saisi l'élément et appuyé sur ENTRER
		searchBox.send_keys(Keys.ENTER)
		#On doit arriver sur une liste de résultats  
		recordSearchResultUrl = self.browser.current_url
		self.assertRegex(recordSearchResultUrl, '/records/.+')
		#on vérifie qu'il y a un résultat (should be 'The Fat Of the Land')
		self.check_for_row_in_list_table('The Fat Of The Land')
				
		#Il reste un champ de saisie pour ajouter un vinyle
		# L'utilisateur y ajoute "Invaders Must Die"
		inputbox = self.get_item_input_box()
		inputbox.send_keys('Invaders Must Die')
		inputbox.send_keys(Keys.ENTER)
		# Il arrive sur une page qui lui demande plus d'informations
		recordCreationUrl = self.browser.current_url
		self.assertRegex(recordCreationUrl, '/records/.+')
		#Le titre doit être affiché mais editable
		recordNameField = self.browser.find_element_by_id('record_name_text')
		self.assertIn('Invaders Must Die', recordNameField.text)
		self.add_record('Invaders Must Die',2012,'Prodigy',711297880113)
		
		#L'utilisateur arrive sur la page d'accueil
		endRecordCreationURL = self.browser.current_url
		self.assertRegex(endRecordCreationURL, '/')
		