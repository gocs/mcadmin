from django.shortcuts import render
from django.views.generic import ListView
from .models import Todo

class HomePageView(ListView):
    model = Todo
    template_name = "todo/home.html"