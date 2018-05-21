import csv
from address.constants import (
    API_KEY,
    SUCCESS_MESSAGE,
    UPLOADED_FILE,
    WARNING_MESSAGE
)
from address.forms import DocumentForm
from address.handlers.csv_handlers import CSVHandler
from address.models import Document
from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View
import requests


class HomeView(View):
    def get(self, request):
        documents = Document.objects.all()
        return render(request, 'address/home.html', {'documents': documents})

    def post(self, request):
        post_data = request.POST.dict()
        if 'file_id' not in post_data:
            messages.warning(request, WARNING_MESSAGE)
            documents = Document.objects.all()
            return render(request, 'address/home.html',
                          {'documents': documents})
        elif 'file_id' in post_data:
            doc_obj = Document.objects.get(id=post_data['file_id'])
            CSVHandler().csv_from_excel(doc_obj)
            with open(UPLOADED_FILE, 'r') as csvfile:
                reader = csv.reader(csvfile)
                city_info = []
                for row in reader:
                    address = row[0]
                    api_key = API_KEY
                    api_response = requests.get(
                        'https://maps.googleapis.com/maps/api/geocode/json?'
                        'address={0}&key={1}'.format(address, api_key))
                    api_response_dict = api_response.json()
                    if api_response_dict['status'] == 'OK':
                        latitude = (
                            api_response_dict['results'][0]['geometry']
                            ['location']['lat'])
                        longitude = (
                            api_response_dict['results'][0]['geometry']
                            ['location']['lng'])
                        city_info_data = {
                            'address': address,
                            'latitude': latitude,
                            'longitude': longitude
                        }
                        city_info.append(city_info_data)
                CSVHandler().generate_excel_file(doc_obj, city_info)
                messages.success(request, SUCCESS_MESSAGE)
        documents = Document.objects.all()
        return render(request, 'address/home.html', {'documents': documents})


class ModelView(View):
    def get(self, request):
        form = DocumentForm()
        return render(request, 'address/model_form_upload.html', {
            'form': form
        })

    def post(self, request):
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
