from django.shortcuts import render
from django.shortcuts import redirect

def is_admin(user):
    return user.groups.filter(name='Admin').exists()

def is_operador(user):
    return user.groups.filter(name='Operador').exists()

def home(request):
    return redirect('/dashboard/')