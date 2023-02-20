from django.views.generic import TemplateView, UpdateView, CreateView
from django.shortcuts import render, redirect, reverse


class HomeView(TemplateView):
    template_name = "home_user.html"



