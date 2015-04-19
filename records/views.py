from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ValidationError
from records.forms import (
	RecordForm,ArtistForm,MinimalRecordForm,RecordSearchForm,
	EMPTY_ITEM_ERROR,DUPLICATE_ITEM_ERROR,
	ExistingArtistRecordForm,MinimalArtistForm
	)
from records.models import Record, Artist


def home_page(request):
	artists = Artist.objects.all()
	minimalRecordForm=MinimalRecordForm()
	minimalArtistForm=MinimalArtistForm()
	recordSearchForm = RecordSearchForm()
	return render(request, 'home.html',{
		'artists':artists,
		'minimalRecordForm':minimalRecordForm,
		'minimalArtistForm':minimalArtistForm,
		'recordSearchForm': recordSearchForm})

def view_record(request,record_id):
	#We retrieve the record object from the URL
	record = get_object_or_404(Record,id=record_id)
	minimalRecordForm=MinimalRecordForm()
	minimalArtistForm=MinimalArtistForm()
	#we retrieve the artist ID from the POST
	form = ExistingArtistRecordForm(request.POST or None,instance=record)
	if form.is_valid():
		form.save()
		return redirect(record)
	return render(request, 'record.html',{
		'record':record,
		'form':form,
		'minimalRecordForm':minimalRecordForm,
		'minimalArtistForm': minimalArtistForm})
def new_record(request):
	form = RecordForm(data=request.POST)
	minimalRecordForm=MinimalRecordForm()
	minimalArtistForm=MinimalArtistForm()
	#we retrieve the artist ID from the POST
	if form.is_valid():
		#record = Record.objects.create()
		record = form.save()

		return redirect(record)
	else:
		return render(request, 'home.html',{
			"form":form,
			'minimalRecordForm': minimalRecordForm,
			'minimalArtistForm': minimalArtistForm})
def view_artist(request,artist_id):
	artist = get_object_or_404(Artist,id=artist_id)
	minimalRecordForm=MinimalRecordForm()
	minimalArtistForm=MinimalArtistForm()
	form = ArtistForm(request.POST or None,instance=artist)
	if form.is_valid():
		form.save()
		return redirect(artist)
	return render(request, 'artist.html',{
		'artist':artist,
		'form':form,
		'minimalRecordForm': minimalRecordForm,
		'minimalArtistForm': minimalArtistForm})
def new_artist(request):
	form = ArtistForm(data=request.POST)
	if form.is_valid():
		record = form.save()
		return redirect(record)
	else:
		minimalRecordForm=MinimalRecordForm()
		minimalArtistForm=MinimalArtistForm()
		return render(request, 'home.html',{
			"form":form,
			'minimalRecordForm': minimalRecordForm,
			'minimalArtistForm': minimalArtistForm})

