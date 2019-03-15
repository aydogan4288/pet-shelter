
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from .models import User, Item
import bcrypt

def index(request):

    return render(request, 'myapp/index.html')

def register(request):

    print(request.POST)
    errors = User.objects.register_validator(request.POST)

    if len(errors):
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error, extra_tags='register')
        return redirect('/')

    else:
        password = request.POST['password']
        password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password = password)
        request.session['user_id'] = user.id
        return redirect('/dash')

def login(request):
    print(request.POST)
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error, extra_tags='login')
        return redirect('/')

    else:
        user = User.objects.get(username=request.POST['usernamelogin'])
        request.session['user_id'] = user.id
        return redirect('/dash')

def dash(request):

    if 'user_id' not in request.session:
        return redirect('/')
    else:
        other_items = []
        all_items = Item.objects.all()
        myitems = User.objects.get(id=request.session['user_id']).faved_items.all()
        for item in all_items:
            if item not in myitems:
                other_items.append(item)

        context = {
            "items": other_items,
            "user" : User.objects.get(id= request.session['user_id']),
            "myitems": myitems,
        }
        return render(request, "myapp/dash.html", context)

def create(request):
    errors = Item.objects.item_validator(request.POST)
    if errors:
        for key, error in errors.items():
            messages.add_message(request, messages.ERROR, error)
        print(errors)
        return redirect('/new')
    else:
        print(request.POST)
        item = Item.objects.create(product=request.POST["product"], creater_id = request.session['user_id'])
        item.faved_users.add(User.objects.get(id=request.session['user_id']))
        return redirect('/dash')

def new(request):
    return render(request, 'myapp/new.html')

def show(request, itemid):
    item = Item.objects.get(id=itemid)
    users = item.faved_users.all()
    context = {
    'item': item,
    'users': users,
    }
    return render(request, 'myapp/show.html', context)

def join(request, itemid):
    item = Item.objects.get(id=itemid)
    item.faved_users.add(User.objects.get(id= request.session['user_id']))
    users = item.faved_users.all()

    context = {
    'item': item,
    'users': users,
    }
    return render(request, 'myapp/show.html', context)

def cancel(request, itemid):
    item = Item.objects.get(id=itemid)
    item.faved_users.remove(User.objects.get(id=request.session['user_id']))
    return redirect('/dash')

def delete(request, itemid):
    Item.objects.get(id=itemid).delete()
    return redirect ('/dash')


def logout(request):
    request.session.clear()
    return redirect('/')
