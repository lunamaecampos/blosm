from django.shortcuts import render, HttpResponse, redirect
from models import User, Album
from .forms import AlbumImageUploadForm
from django.urls import reverse
from django.contrib import messages
from datetime import date, datetime

# Create your views here.
def index(request):
    return render(request,'blosm_app/index.html')

def dashboard(request):
    try:
		request.session['theuser']
                print request.session['userid']
    except KeyError:
        return redirect('/')
    album = Album.objects.order_by('-albumreleasedate')
    context={
		'album': album,
	}
    return render(request, 'blosm_app/dashboard.html', context)

def login(request):
    if request.method =="POST":
        user = User.objects.login(request.POST)
        if 'errors' in user:
            for error in user['errors']:
                messages.error(request, error)
                return redirect('/')
        if 'theuser' in user:
            request.session['theuser'] = user['theuser']
            request.session['userid'] = user['userid']
            return redirect('/dashboard')
def register(request):
    if request.method=="POST":
        user = User.objects.register(request.POST)
    if 'errors' in user:
        for error in user['errors']:
            messages.error(request, error)
        return redirect('/')
    if 'theuser' in user:
        request.session['theuser'] = user['theuser']
        request.session['userid'] = user['userid']
        return redirect('/dashboard')
def logout(request):
    del request.session['theuser']
    del request.session['userid']
    return redirect('/')

def createAlbum(request, id):
    if request.method == 'POST':
        print id
        album = Album.objects.createAlbum(request.POST, id=id)
        form = AlbumImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            a = Album.objects.get(pk=id)
            a.albumart = form.cleaned_data['albumart']
            a.save()
            return redirect('/dashboard')
    return HttpResponseForbidden('allowed only via POST')

def deleteAlbum(request,id):
    Album.objects.deleteAlbum(id=id)
    return redirect('/dashboard')
