from haystack.views import basic_search
from records.forms import (
	RecordForm,ArtistForm,MinimalRecordForm, EMPTY_ITEM_ERROR,
	DUPLICATE_ITEM_ERROR,ExistingArtistRecordForm,
	MinimalArtistForm
	)


def search_view(request):
	minimalRecordForm=MinimalRecordForm()
	minimalArtistForm=MinimalArtistForm()
	
	return basic_search(request, extra_context={
		'minimalRecordForm': minimalRecordForm,
		'minimalArtistForm': minimalArtistForm})

