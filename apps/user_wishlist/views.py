from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from time import strftime

from .models import User, Item

def index(request):
    return render(request, "user_wishlist/index.html")

def register(request):
    if request.method == 'POST':
        check = User.objects.validate_date(request.POST)
        if isinstance(check, unicode):
            messages.error(request, check)
            return redirect('/')
        result = User.objects.validate_registration(request.POST)
        if isinstance(result,list):
            for error in result:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['id'] = result
            return redirect('/dashboard')
    else:
        return redirec('/')

def login(request):
    if request.method == 'POST':
        result = User.objects.validate_login(request.POST)
        if isinstance(result, list):
            for error in result:
                messages.error(request, error)
            return redirect('/')
        else:
            request.session['id'] = result
            return redirect('/dashboard')
    else:
        return redirect('/')

def home(request):
    if 'id' not in request.session:
        messages.error(request, "You must be logged in to view this page")
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['id']),
            'user_items': Item.objects.filter(created_by=request.session['id']) | Item.objects.filter(added_by=request.session['id']),
            'other_items': Item.objects.all().exclude(created_by=request.session['id']).exclude(added_by=request.session['id']),
            'create_date': strftime("%B %d %Y")
            }
    return render(request, "user_wishlist/home.html", context)

def wish_item(request):
    if 'id' not in request.session:
        messages.error(request, "You must be logged in to view this page")
        return redirect('/')
    else:
        return render(request, "user_wishlist/item_create.html")

def create(request):
    if request.method == 'POST':
        result = Item.objects.validate_item(request.POST, request.session['id'])
        if isinstance(result, list):
            for error in result:
                messages.error(request, error)
            return redirect('/wish_item')
        else:
            return redirect('/dashboard')

def show_item(request, item_id):
    if 'id' not in request.session:
        messages.error(request, "You must be logged in to view this page")
        return redirect('/')
    else:
        context = {
            'item': Item.objects.get(id=item_id),
            'creator': User.objects.filter(created_items=Item.objects.get(id=item_id)),
            'users': User.objects.filter(added_items=Item.objects.get(id=item_id)),
            }
    print context
    return render(request, "user_wishlist/wish_item.html", context)

def add(request, item_id):
    Item.objects.get(id=item_id).added_by.add(User.objects.get(id=request.session['id']))
    return redirect('/dashboard')

def remove(request, item_id):
    Item.objects.get(id=item_id).added_by.remove(User.objects.get(id=request.session['id']))
    return redirect('/dashboard')

def delete(request, item_id):
    Item.objects.get(id=item_id).delete()
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')
