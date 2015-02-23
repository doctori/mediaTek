from django.shortcuts import render,redirect
from django.core.exceptions import ValidationError
from records.forms import (
	RecordForm, EMPTY_ITEM_ERROR,
	DUPLICATE_ITEM_ERROR,ExistingRecordItemForm
	)
from records.models import Record, Artist

def home_page(request):
	return render(request, 'home.html',{'form':RecordForm()})

def view_record(request,record_id):
	#We retrieve the list object from the URL
	record = Record.objects.get(id=record_id)
	form = ExistingRecordItemForm(for_record=record)
	if request.method == 'POST':
		form = ExistingRecordItemForm(for_record=record,data=request.POST)
		if form.is_valid():
			form.save()
			return redirect(list_)
	return render(request, 'record.html',{'record':record, 'form':form})

def new_record(request):
	form = RecordForm(data=request.POST)
	if form.is_valid():
		record = Record.objects.create()
		form.save(for_artist=artist)
		return redirect(record)
	else:
		return render(request, 'home.html',{"form":form})