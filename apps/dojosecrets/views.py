from django.shortcuts import render, redirect, reverse
from . import models
from django.contrib import messages
from django.db.models import Count
import bcrypt

# Create your views here.
def index(request):
    return render(request, "dojosecrets/index.html")

def register(request):
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']
    password = request.POST['password']
    confirm = request.POST['confirm']
    registered = models.User.objects.register(request, first_name, last_name, email, password, confirm)
    if (registered):
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        query = models.User(first_name = first_name, last_name = last_name, email = email, password_hash = hashed)
        query.save()
        user_id = query.pk
        return redirect(reverse('secret',  kwargs={'user_id': query.pk }))
    else:
        return redirect(reverse("index"))

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = models.User.objects.all().get(email = email)
    if bcrypt.hashpw(password.encode(), user.password_hash.encode()) == user.password_hash.encode():
        user_id = user.pk
        return redirect(reverse('secret',  kwargs={'user_id': user.pk } ))
    else:
        messages.error(request, "Unable to log in!")
        return redirect(reverse("index"))

def secret(request, user_id):
    user = models.User.objects.all().get(pk = user_id)
    name = user.first_name
    secrets = models.Secret.objects.all()
    user_secrets = models.User.objects.all()
    secret_dict = {}
    liker_dict = {}
    for secret in secrets:
        likes = secret.likes.count()
        likers = secret.likes.all()
        liker_list = []
        for liker in likers:
            liker_list.append(liker.first_name)
        secret_dict[secret.pk] = likes
        liker_dict[secret.pk] = liker_list
    print liker_dict
    context = {
        'name' : name,
        'user_id' : int(user_id),
        'secrets' : secrets,
        'secret_dict' : secret_dict,
        'liker_dict' : liker_dict
    }
    return render(request, 'dojosecrets/home.html', context)

def secret_add(request, user_id):
    secret = request.POST['secret']
    user = models.User.objects.all().get(pk = user_id)
    secret_query = models.Secret(secret = secret, user = user)
    secret_query.save()
    return redirect(reverse("secret",  kwargs={'user_id': user_id }))

def like(request, user_id):
    secret_id = request.POST['secret_id']
    models.User.objects.add_like(secret_id, user_id)
    return redirect(reverse("secret",  kwargs={'user_id': user_id }))
