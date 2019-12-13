from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Wish, Like
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register_verify(request):
    errors = User.objects.basic_validator_user(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    elif request.POST['password_confirm'] != request.POST['password']:
        messages.error(request, 'The password entered twice must be the same!')
        return redirect('/')
    else:
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        user_pwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        this_user = User.objects.create(email=email, first_name=first_name, last_name=last_name, password=user_pwd)
        request.session['this_user_id'] = this_user.id
        first_user = User.objects.first()
        first_user.user_level = 9
        messages.success(request, "Register successfully!")
        return redirect('/wishes')

def login_verify(request):
    found_user = User.objects.filter(email=request.POST['email'])
    if len(found_user) < 1:
        messages.error(request, 'Invalid Credentials')
        return redirect('/')
    else:
        logged_user = found_user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['this_user_id'] = logged_user.id
            messages.success(request, "Successfully Logg-In")
            return redirect('/wishes')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def wishes(request):
    this_id = request.session.get('this_user_id')
    this_user = User.objects.get(id = this_id)
    context={
        "this_user":this_user,
        "user_wishes":this_user.wishes.all(),
        "granted_wishes":Wish.objects.filter(granted=True)
    }
    return render(request, 'wishes.html', context)

def user_stats(request):
    this_id = request.session.get('this_user_id')
    this_user = User.objects.get(id = this_id)

    total_wish = Wish.objects.all()
    total_wish_count = 0
    for wish in total_wish:
        total_wish_count += 1
    
    user_total_wish = total_wish.filter(user = this_user)
    user_total_wish_count = 0
    for wish in user_total_wish:
        user_total_wish_count += 1

    total_granted_wish = Wish.objects.filter(granted = True)
    user_granted_wish = total_granted_wish.filter(user = this_user)
    user_granted_wish_count = 0
    for wish in user_granted_wish:
       user_granted_wish_count += 1

    user_ungranted_wish_count = user_total_wish_count - user_granted_wish_count
    if user_ungranted_wish_count < 0:
        user_ungranted_wish_count = 0
    context={
        "this_user":this_user,
        "total_wish_count":total_wish_count,
        "granted_wish_count":user_granted_wish_count,
        "ungranted_wish_count":user_ungranted_wish_count
    }
    return render(request, 'user_stats.html', context)

def like(request, id):
    this_id = request.session.get('this_user_id')
    this_user = User.objects.get(id = this_id)
    this_wish = Wish.objects.get(id = id)
    InorNot = this_wish.likes.filter(user=this_user)
    if InorNot:
        return redirect('/wishes')
    else:
        this_like = Like.objects.create(user=this_user, wish=this_wish)
        this_wish.like += 1
        this_wish.save()
        return redirect('/wishes')

def wish_new(request):
    return render(request, 'wish_new.html')

def wish_new_verify(request):
    this_id = request.session.get('this_user_id')
    this_user = User.objects.get(id = this_id)
    if this_user is not None:
        errors = Wish.objects.basic_validator_wish(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wishes/new')
        else:
            item = request.POST['item']
            description = request.POST['description']
            new_wish = Wish.objects.create(item=item, description=description, user=this_user)
            messages.success(request, "Add wish successfully!")
            return redirect('/wishes')
    else:
        return redirect('/')

def wish_granted(request, id):
    this_id = request.session.get('this_user_id')
    this_user = User.objects.get(id = this_id)
    if this_user is not None:
        this_wish = Wish.objects.get(id = id)
        this_wish.granted = True
        this_wish.save()
        return redirect('/wishes')
    else:
        return redirect('/')

def wish_remove(request, id):
    this_id = request.session.get('this_user_id')
    this_user = User.objects.get(id = this_id)
    if this_user is not None:
        this_wish = Wish.objects.get(id = id)
        this_wish.delete()
        return redirect('/wishes')
    else:
        return redirect('/')

def wish_edit(request, id):
    this_id = request.session.get('this_user_id')
    this_user = User.objects.get(id = this_id)
    if this_user is not None:
        this_wish = Wish.objects.get(id = id)
        context={
            "this_wish":this_wish
        }
        return render(request, 'edit_wish.html', context)
    else:
        return redirect('/')

def wish_edit_verify(request, id):
    this_id = request.session.get('this_user_id')
    this_user = User.objects.get(id = this_id)
    if this_user is not None:
        errors = Wish.objects.basic_validator_wish(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
                return redirect('/')
        else:
            this_wish = Wish.objects.get(id = id)
            this_wish.item = request.POST['item']
            this_wish.description = request.POST['description']
            this_wish.user = this_user
            this_wish.save()
            return redirect('/wishes')
    else:
        return redirect('/')