from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
import os

from .forms import ClassifierForm
from .models import Classifier

# Path to input image
media_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'media_cdn/images')

# Model names
indian_model_name = 'pneumonia'
western_model_name = 'malaria'

# Create your views here.

def index(request):
    return render(request, 'classifier/index.html')


def about(request):
    return render(request, 'classifier/about.html')

def upload_img(request):
    form = ClassifierForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        m = Classifier()
        m.image = form.cleaned_data['image']
        print(type(form.cleaned_data['image']))
        print("TYPE: " + form.cleaned_data['category'])
        m.save()
        
        category = form.cleaned_data['category']
        return HttpResponseRedirect('/classifier/predict/?category=' + category)

    return render(request, 'classifier/upload_img.html', {'form': form})


def predict(request):
    # Preprocess image
    img_path = os.path.join(media_path, os.listdir(media_path)[0])
    print(img_path)
    print(request.GET.get('category'))


    return render(request, 'classifier/result.html')


def clean_path(request):
    '''Cleans up image path'''
    # Delete image instance from model
    Classifier.objects.all().delete()

    # Delete image from media directory
    for img in os.listdir(media_path):
        os.remove(os.path.join(media_path, img))

    return HttpResponseRedirect('/')


