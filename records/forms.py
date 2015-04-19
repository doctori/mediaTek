from django import forms
from django.core.exceptions import ValidationError
from records.models import Record, Artist
from haystack.forms import SearchForm

EMPTY_ITEM_ERROR = 'Impossible d\'avoir un élement Vide'
DUPLICATE_ITEM_ERROR = "L'element existe déjà"
class RecordSearchForm(SearchForm):
	def no_query_found(self):
		return self.searchqueryset.all()
		
class RecordForm(forms.models.ModelForm):
	class Meta:
		model = Record
		fields = ('name','year','artist','ean')
		widgets= {
			'name': forms.fields.TextInput(attrs={
			'placeholder': 'Name of the Record',
			'class': "form-control input-lg",
			}),
		}
		error_messages = {
			'name': {'required':EMPTY_ITEM_ERROR},
			'ean': {'required':EMPTY_ITEM_ERROR}
		}
	def save(self):
		return super().save()
class MinimalRecordForm(forms.models.ModelForm):
	class Meta:
		model = Record
		fields = ('name','artist','ean')
		widgets= {
			'name': forms.fields.TextInput(attrs={
			'placeholder': 'Name of the Record',
			'class': "form-control input-lg",
			}),
		}
		error_messages = {
			'name': {'required':EMPTY_ITEM_ERROR}
		}
	def save(self):
		return super().save()
class MinimalArtistForm(forms.models.ModelForm):
	class Meta:
		model = Artist
		fields = ('name',)
		widgets= {
			'name': forms.fields.TextInput(attrs={
			'placeholder': 'Name of the Artist',
			'class': "form-control input-lg",
			}),
		}
		error_messages = {
			'name': {'required':EMPTY_ITEM_ERROR}
		}
	def save(self):
		return super().save()


class ExistingArtistRecordForm(RecordForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
	def save(self):
		return forms.models.ModelForm.save(self)
	def validate_unique(self):
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'name': [DUPLICATE_ITEM_ERROR]}
			self._update_errors(e)

class ArtistForm(forms.models.ModelForm):
	class Meta:
		model = Artist
		fields = ('name',)
		widgets= {
			'name': forms.fields.TextInput(attrs={
			'placeholder': 'Name of the Artist',
			'class': "form-control input-lg",
			}),
		}
		error_messages = {
			'name': {'required':EMPTY_ITEM_ERROR},
		}
		
		
