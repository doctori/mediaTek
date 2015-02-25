from django.shortcuts import render,redirect,get_object_or_404
from django.core.exceptions import ValidationError
from records.forms import (
	RecordForm, EMPTY_ITEM_ERROR,
	DUPLICATE_ITEM_ERROR,ExistingRecordItemForm
	)
from records.models import Record, Artist

def home_page(request):
	return render(request, 'home.html',{'form':RecordForm()})

def view_record(request,record_id):
	#We retrieve the record object from the URL
	record = get_object_or_404(Record,id=record_id)
	form = ExistingRecordItemForm(request.POST or None,instance=record)
	if form.is_valid():
		form.save()
		return redirect(record)
	return render(request, 'record.html',{'record':record, 'form':form})

def new_record(request):
	form = RecordForm(data=request.POST)
	if form.is_valid():
		#record = Record.objects.create()
		#form.save(for_artist=artist)
		record = form.save()
		return redirect(record)
	else:
		return render(request, 'home.html',{"form":form})