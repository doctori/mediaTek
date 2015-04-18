import datetime
from haystack import indexes
from .models import Record,Artist

class RecordIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	content_auto = indexes.EdgeNgramField(model_attr='name')
#    artist = indexes.CharField(model_attr='artist')
#    year = indexes.DateTimeField(model_attr='year')
#    ean = indexes.BigIntegerField(model_attr='ean')

	def get_model(self):
		return Record

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.all()
