from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from WebApp.models import Domains
from django.contrib.auth.models import User

# Create your views here.
from .forms import CreateUserForm
import csv


@login_required(login_url='login')
def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, "Account was created for " + user)
    context = {'form': form}
    return render(request, 'register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main')
            else:
                messages.info(request, 'Username or Password is incorrect !')

        context = {}
        return render(request, 'login.html', context)


@login_required(login_url='login')
def logout_page(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def main_page(request):
    context = {}
    return render(request, 'main.html', context)


@login_required(login_url='login')
def get_main_data(request):
    dict = {}
    index = 0
    filename = '/home/ubuntu/Documents/Licenta/FINALE/logs.log'
    with open(filename, 'r') as data:
        for line in csv.reader(data):
            dict[index] = {
                "date": line[0],
                "user_ip": line[1],
                "action": line[2],
                "domain": line[3],
                "domain_status": line[4]
            }
            index += 1

    context = {"main_data": list(dict.values())}
    return JsonResponse(context)


@login_required(login_url='login')
def view_blacklist(request):
    domains = Domains.objects.all()
    context = {'domains': domains}
    return render(request, 'view_blacklist.html', context)


@login_required(login_url='login')
def view_users_page(request):
    users = User.objects.all()
    context = {"users": users}
    return render(request, 'view_users.html', context)


@login_required(login_url='login')
def user_del(request, username):
    u = User.objects.get(username=username)
    u.delete()
    return redirect('view_users')


@login_required(login_url='login')
def logged_data_page(request):
    dict = {}
    index = 0
    weird_char1 = '\xfe'
    weird_char2 = '\xBF'
    filename = '/home/ubuntu/Documents/Licenta/FINALE/logData.log'
    with open(filename, 'r') as data:
        for line in csv.reader(data):
            dict[index] = {
                "date": line[0],
                "user_ip": line[1],
                "method": line[2],
                "host": line[3],
                "data": line[4].replace(weird_char1, '\r\n').replace(weird_char2, ',')
            }
            index += 1

    context = {"log_data": list(dict.values())}
    return render(request, 'logged_data.html', context)
