from django import forms
from django.core.exceptions import ValidationError
from records.models import Record, Artist

EMPTY_ITEM_ERROR = 'Impossible d\'avoir un élement Vide'
DUPLICATE_ITEM_ERROR = "L'element existe déjà"
class RecordForm(forms.models.ModelForm):
	class Meta:
		model = Record
		fields = ('name',)
		widgets= {
			'name': forms.fields.TextInput(attrs={
			'placeholder': 'Name of the Record',
			'class': "form-control input-lg",
			}),
		}
		error_messages = {
			'name': {'required':EMPTY_ITEM_ERROR}
		}
	def save(self,for_artist):
		self.instance.artist = for_artist
		return super().save()
class ExistingRecordItemForm(RecordForm):
	def __init__(self,for_artist, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.artist = for_artist
	def save(self):
		return forms.models.ModelForm.save(self)
	def validate_unique(self):
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
			self._update_errors(e)
