import logging
from haystack.views import basic_search
from haystack.query import EmptySearchQuerySet, SearchQuerySet
from haystack.inputs import Clean
from records.forms import (
	RecordForm,ArtistForm,RecordSearchForm,
	MinimalRecordForm,MinimalArtistForm
	)
from django.shortcuts import render_to_response


def search_view(request): 
	#sqs = SearchQuerySet().filter(content__contains=Clean(request.GET['q']))
	sqs = SearchQuerySet().all()
	form = RecordSearchForm(request.GET)
	records = form.search()
	minimalRecordForm=MinimalRecordForm()
	minimalArtistForm=MinimalArtistForm()
	
	return render_to_response('search.html',{
		'minimalRecordForm': minimalRecordForm,
		'minimalArtistForm': minimalArtistForm,
		'records': records})

